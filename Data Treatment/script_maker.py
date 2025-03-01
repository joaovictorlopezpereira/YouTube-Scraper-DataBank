import os

caminho_pasta = 'csvzinhos'
arquivos = [arquivo for arquivo in os.listdir(caminho_pasta) if os.path.isfile(os.path.join(caminho_pasta, arquivo))]
with open('population.sql', 'w') as txt:  # 'w' cria o arquivo ou sobrescreve se já existir
    for arquivo in arquivos:
      data = arquivo[0:8]
      país = arquivo[9:11]
      txt.write(f'''LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/{data}_{país}_canal.csv'
IGNORE -- Ignora linhas com chaves primárias repetidas
INTO TABLE canal
FIELDS TERMINATED BY ',' -- Delimitador de campo, ex.: vírgula
ENCLOSED BY '"'          -- Delimitador de texto, ex.: aspas duplas
LINES TERMINATED BY '\\n' -- Delimitador de linha, ex.: nova linha
IGNORE 1 ROWS;           -- Ignora a primeira linha, se for cabeçalho

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/{data}_{país}_pais.csv'
IGNORE
INTO TABLE pais
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/{data}_{país}_canal_snapshot.csv'
IGNORE
INTO TABLE canal_snapshot
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/{data}_{país}_video.csv'
IGNORE
INTO TABLE video
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/{data}_{país}_palavra_chave.csv'
IGNORE
INTO TABLE palavra_chave
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/{data}_{país}_video_snapshot.csv'
IGNORE
INTO TABLE video_snapshot
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/{data}_{país}_tag.csv'
IGNORE
INTO TABLE tag
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/{data}_{país}_trend.csv'
IGNORE
INTO TABLE trend
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\\n'
IGNORE 1 ROWS;''')