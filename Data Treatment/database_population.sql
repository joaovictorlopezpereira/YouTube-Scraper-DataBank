-- AVISO: CERTIFIQUE-SE DE QUE O SCRIPT EM 'database_init' JÁ TENHA SIDO EXECUTADO!

USE youtube;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/24.15.11_ZA_canal.csv' 
IGNORE -- Ignora linhas com chaves primárias repetidas
INTO TABLE canal
FIELDS TERMINATED BY ',' -- Delimitador de campo, ex.: vírgula
ENCLOSED BY '"'          -- Delimitador de texto, ex.: aspas duplas
LINES TERMINATED BY '\n' -- Delimitador de linha, ex.: nova linha
IGNORE 1 ROWS;           -- Ignora a primeira linha, se for cabeçalho

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/24.15.11_ZA_pais.csv' 
IGNORE
INTO TABLE pais
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/24.15.11_ZA_canal_snapshot.csv'
IGNORE
INTO TABLE canal_snapshot
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/24.15.11_ZA_video.csv' 
IGNORE
INTO TABLE video
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/24.15.11_ZA_palavra_chave.csv' 
IGNORE
INTO TABLE palavra_chave
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/24.15.11_ZA_video_snapshot.csv'
IGNORE
INTO TABLE video_snapshot
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/24.15.11_ZA_tag.csv' 
IGNORE
INTO TABLE tag
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/24.15.11_ZA_trend.csv'
IGNORE
INTO TABLE trend
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;