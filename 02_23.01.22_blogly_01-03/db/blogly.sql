
DROP DATABASE IF EXISTS blogly;

CREATE DATABASE blogly;

\c blogly

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(35) NOT NULL,
    last_name VARCHAR(35) NOT NULL,
    image_url TEXT DEFAULT NULL
);

INSERT INTO users
  (first_name, last_name, image_url)
VALUES
    ('John', 'Zhang', 'https://upload.wikimedia.org/wikipedia/en/9/96/Meme_Man_on_transparent_background.webp'),
    ('Subject', 'A', NULL),
    ('Carolijn', 'W', NULL);