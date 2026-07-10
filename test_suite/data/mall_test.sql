CREATE DATABASE IF NOT EXISTS mall_test;
USE mall_test;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    role VARCHAR(20)
);

INSERT INTO users (username, role) VALUES ('tester', 'qa');