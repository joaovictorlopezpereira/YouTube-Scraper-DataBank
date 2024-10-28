CREATE TABLE Video (
    ID CHAR(11) PRIMARY KEY,
    Canal_ID CHAR(24),
    Data_hora_de_publicacao DATE,
    Categoria_ID INT
);

CREATE TABLE Categoria (
    ID INT PRIMARY KEY,
    Nome VARCHAR(30)
);

CREATE TABLE Canal (
    ID CHAR(24) PRIMARY KEY,
    Data_de_criacao DATE
);

CREATE TABLE Pais (
    Codigo CHAR(3) PRIMARY KEY
);

CREATE TABLE Video_Snapshot (
    Titulo VARCHAR(100),
    Numero_de_likes BIGINT,
    Numero_de_visualizacoes BIGINT,
    Descricao TEXT,
    Numero_de_comentarios BIGINT,
    Data DATE,
    Video_ID CHAR(11),
    PRIMARY KEY (Data, Video_ID)
);

CREATE TABLE Canal_Snapshot (
    Titulo VARCHAR(100),
    Numero_de_videos INT,
    Descricao TEXT,
    Imagem_de_perfil TEXT,
    Numero_de_visualizacoes BIGINT,
    Link TEXT,
    Numero_de_inscritos BIGINT,
    Data DATE,
    Canal_ID CHAR(24),
    Pais_Codigo CHAR(3),
    PRIMARY KEY (Data, Canal_ID)
);

CREATE TABLE Tag (
    Video_ID CHAR(11) NOT NULL,
    Tag VARCHAR(500), -- Total limit of 500 characters of all tags for each video
    Video_Snapshot_Data DATE,
    PRIMARY KEY (Video_ID, Tag, Video_Snapshot_Data)
);

CREATE TABLE Palavra_chave (
    Canal_ID CHAR(24) NOT NULL,
    Palavra_chave VARCHAR(500), -- Total limit of 500 characters of all keywords for each channel
    Canal_Snapshot_Data DATE,
    PRIMARY KEY (Canal_ID, Palavra_chave, Canal_Snapshot_Data)
);

CREATE TABLE Trend (
    Pais_Codigo CHAR(3),
    Video_ID CHAR(11),
    Video_Snapshot_Data DATE,
    PRIMARY KEY (Pais_Codigo, Video_ID, Video_Snapshot_Data)
);

ALTER TABLE Video ADD CONSTRAINT FK_Video_Canal_ID
    FOREIGN KEY (Canal_ID)
    REFERENCES Canal (ID)
    ON DELETE RESTRICT;

ALTER TABLE Video ADD CONSTRAINT FK_Video_Categoria_ID
    FOREIGN KEY (Categoria_ID)
    REFERENCES Categoria (ID)
    ON DELETE RESTRICT;

ALTER TABLE Video_Snapshot ADD CONSTRAINT FK_Video_Snapshot_Video_ID
    FOREIGN KEY (Video_ID)
    REFERENCES Video (ID)
    ON DELETE CASCADE;

ALTER TABLE Canal_Snapshot ADD CONSTRAINT FK_Canal_Snapshot_Canal_ID
    FOREIGN KEY (Canal_ID)
    REFERENCES Canal (ID)
    ON DELETE CASCADE;

ALTER TABLE Canal_Snapshot ADD CONSTRAINT FK_Canal_Snapshot_Pais_Codigo
    FOREIGN KEY (Pais_Codigo)
    REFERENCES Pais (Codigo)
    ON DELETE RESTRICT;

ALTER TABLE Tag ADD CONSTRAINT FK_Tag_Video_ID
    FOREIGN KEY (Video_ID)
    REFERENCES Video_Snapshot (Video_ID)
    ON DELETE CASCADE;

ALTER TABLE Tag ADD CONSTRAINT FK_Tag_Video_Snapshot_Data
    FOREIGN KEY (Video_Snapshot_Data)
    REFERENCES Video_Snapshot (Data)
    ON DELETE CASCADE;

ALTER TABLE Palavra_chave ADD CONSTRAINT FK_Palavra_chave_Canal_Snapshot_Data
    FOREIGN KEY (Canal_Snapshot_Data)
    REFERENCES Canal_Snapshot (Data)
    ON DELETE CASCADE;

ALTER TABLE Palavra_chave ADD CONSTRAINT FK_Palavra_chave_Canal_ID
    FOREIGN KEY (Canal_ID)
    REFERENCES Canal_Snapshot (Canal_ID)
    ON DELETE CASCADE;

ALTER TABLE Trend ADD CONSTRAINT FK_Trend_Pais_Codigo
    FOREIGN KEY (Pais_Codigo)
    REFERENCES Pais (Codigo)
    ON DELETE RESTRICT;

ALTER TABLE Trend ADD CONSTRAINT FK_Trend_Video_ID
    FOREIGN KEY (Video_ID)
    REFERENCES Video_Snapshot (Video_ID)
    ON DELETE RESTRICT;

ALTER TABLE Trend ADD CONSTRAINT FK_Trend_Video_Snapshot_Data
    FOREIGN KEY (Video_Snapshot_Data)
    REFERENCES Video_Snapshot (Data)
    ON DELETE RESTRICT;