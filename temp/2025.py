import os
import sys
import pandas as pd
import mysql.connector as mysql

MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = ""  # <-- Fill with your MySQL root password if set
MYSQL_DB = "lib_main"

STUDENTS_XLSX = "2025.xlsx"
EMAIL_DOMAIN = "@poornima.edu.in"

def is_valid_email(email: str) -> bool:
    if not isinstance(email, str) or not email:
        return False
    return email.lower().endswith(EMAIL_DOMAIN)

def safe_int(val):
    try:
        if pd.isna(val):
            return None
        return int(str(val).strip().split('.')[0])
    except Exception:
        return None

def safe_str(val):
    if pd.isna(val):
        return ""
    return str(val).strip()

def get_connection():
    try:
        conn = mysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB
        )
        conn.autocommit = True
        return conn
    except mysql.Error as e:
        print(f"[FATAL] MySQL connection failed: {e}")
        sys.exit(1)

def ensure_students_table(cursor):
    students_table = """
    CREATE TABLE IF NOT EXISTS Students (
        full_reg_no VARCHAR(20) PRIMARY KEY, 
        name VARCHAR(100),
        branch VARCHAR(50),
        year INT CHECK (year BETWEEN 1 AND 5),
        email VARCHAR(255) CHECK(email LIKE '%@poornima.edu.in')
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    try:
        cursor.execute(students_table)
    except mysql.Error as e:
        print(f"[ERROR] Creating Students table: {e}")

def import_students(cursor, df):
    inserted = updated = skipped = 0
    errors = []
    insert_sql = """
    INSERT INTO Students (full_reg_no, name, branch, year, email)
    VALUES (%s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        name = VALUES(name),
        branch = VALUES(branch),
        year = VALUES(year),
        email = VALUES(email);
    """
    for idx, row in df.iterrows():
        full_reg_no = safe_str(row.get("full_reg_no"))
        name = safe_str(row.get("name"))
        branch = safe_str(row.get("branch"))
        year = safe_int(row.get("year"))
        email = safe_str(row.get("email"))
        if not full_reg_no:
            skipped += 1
            errors.append(f"students row {idx}: full_reg_no is required.")
            continue
        if year is None or not (1 <= year <= 5):
            skipped += 1
            errors.append(f"students row {idx}: year must be 1-5 (got: {row.get('year')}).")
            continue
        if not is_valid_email(email):
            skipped += 1
            errors.append(f"students row {idx}: email must end with {EMAIL_DOMAIN} (got: {email}).")
            continue
        try:
            cursor.execute(insert_sql, (full_reg_no, name, branch, year, email))
            if cursor.rowcount == 1:
                inserted += 1
            else:
                updated += 1
        except mysql.Error as e:
            skipped += 1
            errors.append(f"students row {idx}: DB error -> {e}")
    return {"inserted": inserted, "updated": updated, "skipped": skipped, "errors": errors}

def main():
    conn = get_connection()
    cursor = conn.cursor()
    ensure_students_table(cursor)
    if not os.path.exists(STUDENTS_XLSX):
        print(f"[FATAL] {STUDENTS_XLSX} not found.")
        sys.exit(1)
    xl = pd.ExcelFile(STUDENTS_XLSX)
    # Students sheet
    if "students" in xl.sheet_names:
        print("\n[INFO] Importing students ...")
        students_df = xl.parse("students")
        students_result = import_students(cursor, students_df)
        print(f"  Inserted: {students_result['inserted']}, Updated: {students_result['updated']}, Skipped: {students_result['skipped']}")
        if students_result["errors"]:
            print("  Issues:")
            for e in students_result["errors"]:
                print("   -", e)
    else:
        print("[WARN] 'students' sheet not found in Excel.")
    cursor.close()
    conn.close()
    print("\n[DONE] Migration completed.")