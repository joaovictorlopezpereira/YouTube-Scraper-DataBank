USE youtube_trending_statistics;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/24.25.10_canal.csv'
INTO TABLE canal
FIELDS TERMINATED BY ',' -- Delimitador de campo, ex.: vírgula
ENCLOSED BY '"'          -- Delimitador de texto, ex.: aspas duplas
LINES TERMINATED BY '\n' -- Delimitador de linha, ex.: nova linha
IGNORE 1 ROWS;           -- Ignora a primeira linha, se for cabeçalho 

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/24.25.10_canal_snapshot.csv'
INTO TABLE canal_snapshot
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/categoria.csv'
INTO TABLE categoria
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY ';'
IGNORE 1 ROWS;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/24.25.10_pais.csv'
INTO TABLE pais
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/24.25.10_palavra_chave.csv'
INTO TABLE palavra_chave
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/24.25.10_tag.csv'
INTO TABLE tag
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/24.25.10_trend.csv'
INTO TABLE trend
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/24.25.10_video.csv'
INTO TABLE video
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/24.25.10_video_snapshot.csv'
INTO TABLE video_snapshot
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;