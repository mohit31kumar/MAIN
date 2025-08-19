CREATE DATABASE library_db;

USE library_db;

-- User master table (from users.xlsx)
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_reg_no VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100),logslogsusersusers
    branch VARCHAR(50),
    year VARCHAR(20),
    email VARCHAR(100),
    role ENUM('Student','Faculty') NOT NULL
);

-- Log table
CREATE TABLE logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_reg_no VARCHAR(50) NOT NULL,
    name VARCHAR(100),
    branch VARCHAR(50),
    year VARCHAR(20),
    email VARCHAR(100),
    entry_date DATE,
    entry_time TIME,
    exit_date DATE,
    exit_time TIME,
    role ENUM('Student','Faculty'),
    reason VARCHAR(100),
    FOREIGN KEY (full_reg_no) REFERENCES users(full_reg_no)
);