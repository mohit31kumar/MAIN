create database library_managment;
use library_managment;

CREATE TABLE Faculty
(
    full_reg_no INT CHECK(full_reg_no BETWEEN 0000 AND 9999) PRIMARY KEY,
    name VARCHAR(250),
    email VARCHAR(255) CHECK (email LIKE '%@poornima.edu.in')
);
CREATE TABLE Students
(
    full_reg_no VARCHAR(20) PRIMARY KEY, 
    name VARCHAR(100),
    branch VARCHAR(50),
    year INT CHECK (year BETWEEN 1 AND 5),
    email VARCHAR(255) CHECK(email LIKE '%@poornima.edu.in')
);
