-- AVISO: RODE ESTE SCRIPT APENAS 1 (UMA) VEZ!

INSERT INTO Pais VALUES 
('US'), 
('BR'), 
('ZA'), 
('FR'), 
('RU'), 
('JP'), 
('AU');

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/categoria.csv'
INTO TABLE categoria
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;