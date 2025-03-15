CREATE DATABASE IF NOT EXISTS TENNIS_RANKING;
USE TENNIS_RANKING;


CREATE TABLE IF NOT EXISTS Competitors (
    competitor_id VARCHAR(50) PRIMARY KEY,  
    name VARCHAR(100) NOT NULL,             
    country VARCHAR(100) NOT NULL,          
    country_code CHAR(3) NOT NULL,          
    abbreviation VARCHAR(10) NOT NULL       
);


CREATE TABLE IF NOT EXISTS Competitor_Rankings (
    rank_id INT AUTO_INCREMENT PRIMARY KEY, 
    `rank` INT NOT NULL,                     
    movement INT NOT NULL,                    
    points INT NOT NULL,                     
    competitions_played INT NOT NULL,        
    competitor_id VARCHAR(50),                
    FOREIGN KEY (competitor_id) REFERENCES Competitors(competitor_id) 
        ON DELETE CASCADE ON UPDATE CASCADE   
);

show tables;


drop table competitor_rankings;
drop table competitors;
select*from competitors;
select*from competitor_rankings;

SELECT c.name, cr.ranks, cr.points
FROM Competitors c
JOIN Competitor_Rankings cr ON c.competitor_id = cr.competitor_id
ORDER BY cr.ranks ASC
LIMIT 10000;

SELECT c.name, cr.ranks, cr.points
FROM Competitors c
JOIN Competitor_Rankings cr ON c.competitor_id = cr.competitor_id
WHERE cr.ranks <= 5
ORDER BY cr.ranks ASC;

SELECT c.name, cr.ranks, cr.points
FROM Competitors c
JOIN Competitor_Rankings cr ON c.competitor_id = cr.competitor_id
WHERE cr.movement = 0
ORDER BY cr.ranks ASC;

SELECT c.country, SUM(cr.points) AS total_points
FROM Competitors c
JOIN Competitor_Rankings cr ON c.competitor_id = cr.competitor_id
WHERE c.country = 'Croatia'
GROUP BY c.country;

SELECT c.country, COUNT(*) AS competitor_count
FROM Competitors c
GROUP BY c.country
ORDER BY competitor_count DESC;

SELECT c.name, cr.rank, cr.points
FROM Competitors c
JOIN Competitor_Rankings cr ON c.competitor_id = cr.competitor_id
ORDER BY cr.points DESC
LIMIT 1;










 