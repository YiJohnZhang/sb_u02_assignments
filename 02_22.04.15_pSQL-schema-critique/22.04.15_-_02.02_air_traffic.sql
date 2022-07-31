-- from the terminal run:
-- psql < air_traffic.sql

DROP DATABASE IF EXISTS air_traffic;

CREATE DATABASE air_traffic;

\c air_traffic

CREATE TABLE airlines
(
  id SERIAL PRIMARY KEY,
  airline_name TEXT NOT NULL UNIQUE
);

CREATE TABLE places
(
  id SERIAL PRIMARY KEY,
  city_name TEXT NOT NULL,
  country_name TEXT NOT NULL,
  UNIQUE (city_name, country_name)   --as long as this isn't "Springfield, United States"
);

CREATE TABLE tickets
(
  id SERIAL PRIMARY KEY,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  seat TEXT NOT NULL, --flight details if there was a concept of a "flight detail": then: airline, orign, destination will be  bundledin that relation "
  departure TIMESTAMP NOT NULL,
  arrival TIMESTAMP NOT NULL,
  airline_key INT NOT NULL REFERENCES airlines(id),
  origin_key INT  NOT NULL REFERENCES places(id),
  destination_key INT NOT NULL REFERENCES places(id)
);

INSERT INTO airlines
  (airline_name)
VALUES
  ('United'),         --1
  ('British Airways'),--2
  ('Delta'),          --3
  ('TUI Fly Belgium'),
  ('Air China'),      --5
  ('Berkie'),         
  ('American Airlines'),
  ('Avianca Brasil'); --8

INSERT INTO places      -- because breaking it down into "cities" and "countries" still requires one to store the country in the "cities" relation
  (city_name, country_name)
VALUES
  ('Washington DC', 'United States'), --1
  ('Seattle', 'United States'),       --2
  ('Tokyo', 'Japan'),                 --3
  ('London', 'United Kingdom'),
  ('Los Angeles', 'United States'),   --5
  ('Las Vegas', 'United States'),
  --('Seattle', 'United States'), (not automatically ignored)
  ('Mexico City', 'Mexico'),          --7
  ('Paris', 'France'),                --8
  ('Casablanca', 'Morocco'),
  ('Dubai', 'UAE'),                   --10
  ('Beijing', 'China'),               --11
  ('New York', 'United States'),
  ('Charlotte', 'United States'),
  ('Cedar Rapids', 'United States'),  --14
  ('Chicago', 'United States'),       --15
  ('New Orleans', 'United States'),
  ('Sao Paolo', 'Brazil'),
  ('Santiago', 'Chile');              --18

INSERT INTO tickets
  (first_name, last_name, seat, departure, arrival, airline_key, origin_key, destination_key)
VALUES
  ('Jennifer', 'Finch', '33B', '2018-04-08 09:00:00', '2018-04-08 12:00:00', 1, 1, 2),
  ('Thadeus', 'Gathercoal', '8A', '2018-12-19 12:45:00', '2018-12-19 16:15:00', 2, 3, 4),
  ('Sonja', 'Pauley', '12F', '2018-01-02 07:00:00', '2018-01-02 08:03:00', 3, 5, 6),
  ('Jennifer', 'Finch', '20A', '2018-04-15 16:50:00', '2018-04-15 21:00:00', 3, 2, 7),
  ('Waneta', 'Skeleton', '23D', '2018-08-01 18:30:00', '2018-08-01 21:50:00', 4, 8, 9),
  ('Thadeus', 'Gathercoal', '18C', '2018-10-31 01:15:00', '2018-10-31 12:55:00', 5, 10, 11),
  ('Berkie', 'Wycliff', '9E', '2019-02-06 06:00:00', '2019-02-06 07:47:00', 1, 12, 13),
  ('Alvin', 'Leathes', '1A', '2018-12-22 14:42:00', '2018-12-22 15:56:00', 7, 14, 15),
  ('Berkie', 'Wycliff', '32B', '2019-02-06 16:28:00', '2019-02-06 19:18:00', 7, 13, 16),
  ('Cory', 'Squibbes', '10D', '2019-01-20 19:30:00', '2019-01-20 22:45:00', 8, 17, 18);