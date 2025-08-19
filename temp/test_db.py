import mysql.connector

try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Your password
        database="lib_main"
    )
    print("✅ Database connection successful!")
    
    cursor = mydb.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print("📋 Tables found:", tables)
    
    cursor.close()
    mydb.close()
    
except mysql.connector.Error as err:
    print("❌ Database error:", err)
except Exception as e:
    print("❌ Other error:", e)
