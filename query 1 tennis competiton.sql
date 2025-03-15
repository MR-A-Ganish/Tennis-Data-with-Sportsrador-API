CREATE DATABASE tennis_competitions;
use tennis_competitions;
show databases;
CREATE TABLE Categories (
    category_id VARCHAR(50) PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL
);
desc categories;
drop table competitions;
CREATE TABLE Competitions (
    competition_id VARCHAR(50) PRIMARY KEY,
    competition_name VARCHAR(100) NOT NULL,
    parent_id VARCHAR(50),  -- Nullable
    type VARCHAR(20) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    category_id VARCHAR(50),  -- Foreign Key

    FOREIGN KEY (category_id) REFERENCES Categories(category_id)
);
select*from competitions;

SELECT c.competition_id, c.competition_name, cat.category_name
FROM Competitions c
JOIN Categories cat ON c.category_id = cat.category_id;

SELECT cat.category_name, COUNT(c.competition_id) AS total_competitions
FROM Competitions c
JOIN Categories cat ON c.category_id = cat.category_id
GROUP BY cat.category_name;

SELECT competition_id, competition_name, type
FROM Competitions
WHERE type = 'doubles';

SELECT competition_id, competition_name
FROM Competitions
WHERE category_id = (SELECT category_id FROM Categories WHERE category_name = 'ITF Men');

SELECT parent.competition_name AS parent_competition, sub.competition_name AS sub_competition
FROM Competitions sub
JOIN Competitions parent ON sub.parent_id = parent.competition_id;

SELECT cat.category_name, c.type, COUNT(c.competition_id) AS competition_count
FROM Competitions c
JOIN Categories cat ON c.category_id = cat.category_id
GROUP BY cat.category_name, c.type
ORDER BY cat.category_name, competition_count DESC;

SELECT competition_id, competition_name
FROM Competitions
WHERE parent_id IS NULL;












