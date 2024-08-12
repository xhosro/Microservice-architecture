-- Drop the user if it exists
DROP USER IF EXISTS 'auth_user'@'localhost';

-- Create the user
CREATE USER 'auth_user'@'localhost' IDENTIFIED BY 'azerty123';

-- Create the database
CREATE DATABASE IF NOT EXISTS auth;

-- Grant privileges to the user on the auth database
GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'localhost';

-- Use the auth database
USE auth;

-- Create the user table
CREATE TABLE IF NOT EXISTS user (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- Insert a new user into the user table
INSERT INTO user (email, password) VALUES ('khosro@mail.com', 'azerty123');


# 