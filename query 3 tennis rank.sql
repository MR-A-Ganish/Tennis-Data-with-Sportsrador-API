create database tennis_rank;
use tennis_rank;

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
);
select*from competitors;
select*from competitor_rankings;

SELECT c.competitor_id, c.name, cr.rank, cr.points
FROM Competitor_Rankings cr
JOIN Competitors c ON cr.competitor_id = c.competitor_id;

SELECT c.competitor_id, c.name, cr.rank, cr.points
FROM Competitor_Rankings cr
JOIN Competitors c ON cr.competitor_id = c.competitor_id
WHERE cr.rank <= 5
ORDER BY cr.rank ASC;

SELECT c.competitor_id, c.name, cr.rank, cr.movement
FROM Competitor_Rankings cr
JOIN Competitors c ON cr.competitor_id = c.competitor_id
WHERE cr.movement = 0;

SELECT c.country, SUM(cr.points) AS total_points
FROM Competitor_Rankings cr
JOIN Competitors c ON cr.competitor_id = c.competitor_id
WHERE c.country = 'Croatia'
GROUP BY c.country;

SELECT c.country, COUNT(c.competitor_id) AS total_competitors
FROM Competitors c
GROUP BY c.country
ORDER BY total_competitors DESC;

SELECT c.competitor_id, c.name, cr.points
FROM Competitor_Rankings cr
JOIN Competitors c ON cr.competitor_id = c.competitor_id
ORDER BY cr.points DESC
LIMIT 1;
