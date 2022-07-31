
DROP DATABASE IF EXISTS blogly_test;

CREATE DATABASE blogly_test;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(35) NOT NULL,
    last_name VARCHAR(35) NOT NULL,
    image_url TEXT DEFAULT NULL
);