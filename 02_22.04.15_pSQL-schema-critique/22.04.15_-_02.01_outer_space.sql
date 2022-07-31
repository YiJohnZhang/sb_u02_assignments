-- from the terminal run:
-- psql < outer_space.sql

DROP DATABASE IF EXISTS outer_space;

CREATE DATABASE outer_space;

\c outer_space

CREATE TABLE galaxy (
	id SERIAL PRIMARY KEY,
	galaxy_name TEXT NOT NULL
);

CREATE TABLE star_system (
	id SERIAL PRIMARY KEY,
	star_name TEXT NOT NULL
);

--https://stackoverflow.com/questions/21766788/postgresql-syntax-error-when-creating-a-table
--  In postgres, names that are not all lowercase need to be double quoted.

CREATE TABLE planets
(
  id SERIAL PRIMARY KEY,
  planet_name TEXT NOT NULL,
  orbital_period_in_years FLOAT NOT NULL,
  star_system_key INT REFERENCES star_system(id),
  galaxy_key INT REFERENCES galaxy(id)
);

CREATE TABLE moons (
	id SERIAL PRIMARY KEY,
	moon_name TEXT NOT NULL,
	planet_key INT REFERENCES planets(id)
);

-- Data Seeding
INSERT INTO galaxy
  (galaxy_name)
VALUES
	('Milky Way');

INSERT INTO star_system
  (star_name)
VALUES
	('The Sun'),
	('Proxima Centauri'),
	('Gliese 876');

INSERT INTO planets
  (planet_name, orbital_period_in_years, star_system_key, galaxy_key)
VALUES
  ('Venus', 0.62, 1, 1),
  ('Earth', 1.00, 1, 1),
  ('Mars', 1.88, 1, 1),
  ('Neptune', 164.8, 1, 1),
  ('Proxima Centauri b', 0.03, 2, 1),
  ('Gliese 876 b', 0.23, 3, 1);
 
INSERT INTO moons
  (moon_name, planet_key)
VALUES
  ('The Moon', 2),
  -- ("The Moon", 2) (LINE 4: COLUMN "The Moon" does not exist). Use single-quotes for string values, double-quotes for table_name/column_name
  ('Phobos',3),
  ('Deimos',3),
  ('Naiad',4),
  ('Thalassa',4),
  ('Despina',4),
  ('Galatea',4),
  ('Larissa',4),
  ('S/2004 N 1',4),
  ('Proteus',4),
  ('Triton',4),
  ('Nereid',4),
  ('Halimede',4),
  ('Sao',4),
  ('Laomedeia',4),
  ('Psamathe',4),
  ('Neso',4);