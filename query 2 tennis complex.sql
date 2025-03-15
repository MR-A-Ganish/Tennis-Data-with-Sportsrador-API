CREATE DATABASE tennis_complexes;
USE tennis_complexes;

CREATE TABLE IF NOT EXISTS Complexes (
    complex_id VARCHAR(50) PRIMARY KEY,
    complex_name VARCHAR(100) NOT NULL
);


CREATE TABLE IF NOT EXISTS Venues (
    venue_id VARCHAR(50) PRIMARY KEY,
    venue_name VARCHAR(100) NOT NULL,
    city_name VARCHAR(100) NOT NULL,
    country_name VARCHAR(100) NOT NULL,
    country_code CHAR(3) NOT NULL,
    timezone VARCHAR(100) NOT NULL,
    complex_id VARCHAR(50),
    FOREIGN KEY (complex_id) REFERENCES Complexes(complex_id)
);

drop table complexes;
drop table venues;
select*from complexes;
select*from venues;

SELECT v.venue_name, v.city_name, v.country_name, c.complex_name
FROM Venues v
JOIN Complexes c ON v.complex_id = c.complex_id;

SELECT c.complex_name, COUNT(v.venue_id) AS number_of_venues
FROM Complexes c
JOIN Venues v ON c.complex_id = v.complex_id
GROUP BY c.complex_name;

SELECT v.venue_name, v.city_name, v.country_name, v.timezone, c.complex_name
FROM Venues v
JOIN Complexes c ON v.complex_id = c.complex_id
WHERE v.country_name = 'Chile';

SELECT v.venue_name, v.city_name, v.country_name, v.timezone
FROM Venues v;

SELECT c.complex_name
FROM Complexes c
JOIN Venues v ON c.complex_id = v.complex_id
GROUP BY c.complex_name
HAVING COUNT(v.venue_id) > 1;

SELECT v.country_name, GROUP_CONCAT(v.venue_name) AS venues
FROM Venues v
GROUP BY v.country_name;

SELECT v.venue_name, v.city_name, v.country_name, v.timezone
FROM Venues v
JOIN Complexes c ON v.complex_id = c.complex_id
WHERE c.complex_name = 'Nacional';















