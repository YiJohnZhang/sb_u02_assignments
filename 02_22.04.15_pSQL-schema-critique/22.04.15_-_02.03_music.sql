-- from the terminal run:
-- psql < music.sql

DROP DATABASE IF EXISTS music;

CREATE DATABASE music;

\c music

CREATE TABLE albums
(
  id SERIAL PRIMARY KEY,
  album_name TEXT NOT NULL
  --, album_year SMALLINT NOT NULL
  --, album_cover TEXT NOT NULL --link
  --, album_artist TEXT
  --, album_publisher TEXT NOT NULL
  --, album_copyright TEXT NOT NULL
);

CREATE TABLE songs
(
  id SERIAL PRIMARY KEY,      --BIGSERIAL b/c 1E19 songs, consider TEXT if the average number of recorded songs in human histroy is 1.43E9 song/alive person @ 7E9 
  title TEXT NOT NULL,
  duration_in_seconds INTEGER NOT NULL,
  release_date DATE NOT NULL
);

CREATE TABLE bands  --probably should change this name to "artists" but I'm too lazy
(
  id SERIAL PRIMARY KEY,      --BIGSERIAL if >2.15E9 relevant,recorded bands
  band_name TEXT NOT NULL UNIQUE
);

CREATE TABLE producers
(
  id SERIAL PRIMARY KEY,      --BIGSERIAL if >2.15E9 recorded producers
  producer_name TEXT NOT NULL UNIQUE
);

CREATE TABLE albums_songs_JOIN
(
  pointer SERIAL PRIMARY KEY,
  album_id INT NOT NULL REFERENCES albums(id),
  song_id INT NOT NULL REFERENCES songs(id)
);

CREATE TABLE songs_bands_JOIN
(
  pointer SERIAL PRIMARY KEY,
  song_id INT NOT NULL REFERENCES songs(id),
  band_id INT NOT NULL REFERENCES bands(id)
);

CREATE TABLE songs_producers_JOIN
(
  pointer SERIAL PRIMARY KEY,
  song_id INT NOT NULL REFERENCES songs(id),
  producer_id INT NOT NULL REFERENCES producers(id)
);

INSERT INTO albums
  (album_name)
VALUES
  ('Middle of Nowhere'),
  ('A Night at the Opera'),
  ('Daydream'),
  ('A Star Is Born'), 
  ('Silver Side Up'),
  ('The Blueprint 3'),
  ('Prism'),
  ('Hands All Over'),
  ('Let Go'),
  ('The Writing''s on the Wall');

INSERT INTO songs
  (title, duration_in_seconds, release_date)
VALUES
  ('MMMBop', 238, '04-15-1997'),              --1
  ('Bohemian Rhapsody', 355, '10-31-1975'),   --2
  ('One Sweet Day', 282, '11-14-1995'),       --3
  ('Shallow', 216, '09-27-2018'),             --4
  ('How You Remind Me', 223, '08-21-2001'),   --5
  ('New York State of Mind', 276, '10-20-2009'),
  ('Dark Horse', 215, '12-17-2013'),          --7
  ('Moves Like Jagger', 201, '06-21-2011'),   --8
  ('Complicated', 244, '05-14-2002'),         --9
  ('Say My Name', 240, '11-07-1999');         --10

INSERT INTO bands
  (band_name)
VALUES
  ('Hanson'),       --1
  ('Queen'),        --2
  ('Mariah Cary'),  --3 (3a)
  ('Boyz II Men'),  --4 (3b)
  ('Bradley Cooper'), --5
  ('Nickelback'),     --6
  ('Jay Z'),          --7 (7a), 6
  ('Alicia Keys'),    --8 (7b), 6
  ('Katy Perry'),     --9 (9a), 7
  ('Juicy J'),        --10 (9b), 7
  ('Maroon 5'),           --11 (11a), 8
  ('Christina Aguilera'), --12 (11b), 8
  ('Avril Lavigne'),      --13, 9
  ('Destiny''s Child');   --14, 10

INSERT INTO producers
  (producer_name)
VALUES
  ('Dust Brothers'),      --1 (1a)
  ('Stephen Lironi'),     --2 (1b)
  ('Roy Thomas Baker'),   --3, 2
  ('Walter Afanasieff'),  --4, 3
  ('Benjamin Rice'),      --5, 4
  ('Rick Parashar'),      --6, 5
  ('Al Shux'),        --7, 6
  ('Max Martin'),     --8 (8a), 7
  ('Cirkut'),         --9 (8b), 7
  ('Shellback'),      --10, 8
  ('Benny Blanco'),   --11 (10b), 8
  ('The Matrix'),     --12, 9
  ('Darkchild');      --13, 10

INSERT INTO albums_songs_JOIN
  (album_id, song_id)
VALUES
  (1,1),
  (2,2),
  (3,3),
  (4,4),
  (5,5),
  (6,6),
  (7,7),
  (8,8),
  (9,9),
  (10,10);

INSERT INTO songs_bands_JOIN
  (song_id, band_id)
VALUES
  (1,1),
  (2,2),
  (3,3),
  (3,4),
  (4,5),
  (5,6),
  (6,7),
  (6,8),
  (7,9),
  (7,10),
  (8,11),
  (8,12),
  (9,13),
  (10,14);

INSERT INTO songs_producers_JOIN
  (song_id, producer_id)
VALUES
  (1,1),
  (1,2),
  (2,3),
  (3,4),
  (4,5),
  (5,6),
  (6,7),
  (7,8),
  (7,9),
  (8,10),
  (8,11),
  (9,12),
  (10,13);