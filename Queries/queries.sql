-- VISÕES AUXILIARES:

-- IDs dos vídeos e suas últimas datas de aparição no Em Alta de cada país
CREATE VIEW Ultima_aparicao_video_pais AS
SELECT V.ID AS Video_ID, T.Pais_Codigo, MAX(VS.Data) AS Ultima_data
FROM Video AS V JOIN
		Video_Snapshot AS VS ON V.ID = VS.Video_ID JOIN
			Trend AS T ON V.ID = T.Video_ID AND
						  VS.Data = T.Video_Snapshot_Data
GROUP BY V.ID, T.Pais_Codigo;

-- IDs dos vídeos e suas últimas datas de aparição no Em Alta
CREATE VIEW Ultima_aparicao_video AS
SELECT Video_ID, MAX(Ultima_Data) AS Ultima_data
FROM Ultima_aparicao_video_pais
GROUP BY Video_ID;

-- IDs dos canais e suas últimas datas de aparição no Em Alta de cada país
CREATE VIEW Ultima_aparicao_canal_pais AS
SELECT C.ID AS Canal_ID, UAVP.Pais_Codigo, MAX(UAVP.Ultima_Data) AS Ultima_data
FROM Ultima_aparicao_video_pais AS UAVP JOIN
		Video AS V ON UAVP.Video_ID = V.ID JOIN
			Canal AS C ON V.Canal_ID = C.ID
GROUP BY C.ID, UAVP.Pais_Codigo;

-- IDs dos canais e suas últimas datas de aparição no Em Alta
CREATE VIEW Ultima_aparicao_canal AS
SELECT Canal_ID, MAX(Ultima_Data) AS Ultima_data
FROM Ultima_aparicao_canal_pais
GROUP BY Canal_ID;

SELECT * FROM Ultima_aparicao_video_pais;
SELECT * FROM Ultima_aparicao_canal_pais;
SELECT * FROM Ultima_aparicao_video;
SELECT * FROM Ultima_aparicao_canal;

-- CONSULTAS:

/*
>> Número de dias coletados
Quantidade de dias que constam no conjunto de dados incorporado.
*/
SELECT COUNT(DISTINCT Data) AS Dias_coletados
FROM Canal_Snapshot;

/*
>> Quantidade de views em alta por canal
Exibe, em ordem decrescente de total de visualizações, os canais que mais tiveram visualizações em seus vídeos em alta durante o período de coleta.
*/
WITH
	Video_mais_recente AS
		(SELECT V.ID, V.Canal_ID, VS.Numero_de_visualizacoes
         FROM Ultima_aparicao_video AS UAV JOIN
					Video AS V ON UAV.Video_ID = V.ID JOIN
						Video_Snapshot AS VS ON V.ID = VS.Video_ID AND
												UAV.Ultima_data = VS.Data)
SELECT DISTINCT CS.Titulo AS Canal, VR.Total_de_visualizacoes
FROM (SELECT Canal_ID, SUM(Numero_de_visualizacoes) AS Total_de_visualizacoes
	  FROM Video_mais_recente
      GROUP BY Canal_ID) AS VR JOIN
		Canal_Snapshot AS CS USING (Canal_ID)
ORDER BY VR.Total_de_visualizacoes DESC;

/*
>> Canais que ficaram no em alta mais vezes
Exibe, em ordem decrescente, os canais que mais apareceram no Em Alta e a quantidade de vezes que isso aconteceu. Consideramos como aparição cada ocorrência de um vídeo do canal no Em Alta de um país em uma data.
*/
SELECT CS.Titulo AS Canal, COUNT(CS.Canal_ID) AS Numero_de_aparicoes
FROM Trend AS T JOIN
		Video_Snapshot AS VS ON T.Video_ID = VS.Video_ID AND
								T.Video_Snapshot_Data = VS.Data JOIN
			Video AS V ON VS.Video_ID = V.ID JOIN
				Canal AS C ON V.Canal_ID = C.ID JOIN
					Canal_Snapshot AS CS ON C.ID = CS.Canal_ID AND
											VS.Data = CS.Data
GROUP BY CS.Titulo
ORDER BY Numero_de_aparicoes DESC;

/*
>> Tags mais utilizadas
Exibe, em ordem decrescente, o número de vezes que uma tag apareceu em algum vídeo em alta. Consideramos como aparição cada ocorrência de uma tag em cada vídeo em sua aparição mais recente em cada Em Alta que esteve.
*/
SELECT Tag, COUNT(Tag) AS Numero_de_usos
FROM Ultima_aparicao_video_pais AS UAVP JOIN
		Tag AS T ON UAVP.Video_ID = T.Video_ID AND
					UAVP.Ultima_data = T.Video_Snapshot_Data
GROUP BY Tag
ORDER BY Numero_de_usos DESC;

/*
>> Palavras-chave mais utilizadas
Exibe, em ordem decrescente, o número de vezes que uma palavra-chave apareceu em algum vídeo em alta. Consideramos como aparição cada ocorrência de uma palavra-chave em cada canal em sua aparição mais recente em cada Em Alta que esteve.
*/
SELECT Palavra_chave, COUNT(Palavra_chave) AS Numero_de_usos
FROM Ultima_aparicao_canal_pais AS UACP JOIN
		Palavra_chave AS PC ON UACP.Canal_ID = PC.Canal_ID AND
							   UACP.Ultima_data = PC.Canal_Snapshot_Data
GROUP BY Palavra_chave
ORDER BY Numero_de_usos DESC;

/*
>> Países (ou não) que mais apareceram no Em Alta
Apresenta cada país e o número de vezes que um canal sediado apareceu no Em Alta. Consideramos como aparição cada ocorrência de canal sediado no país para cada vídeo seu no Em Alta de um país em uma data.
*/
WITH
	Paises_em_alta AS
		(SELECT P.Codigo, CS.Canal_ID
         FROM Canal_Snapshot AS CS LEFT JOIN
				Pais AS P ON CS.Pais_Codigo = P.Codigo JOIN
					Video AS V USING (Canal_ID) JOIN
						Video_Snapshot AS VS ON V.ID = VS.Video_ID AND
												CS.Data = VS.Data JOIN
							Trend AS T ON V.ID = T.Video_ID AND
										  VS.Data = T.Video_Snapshot_Data)
(SELECT Codigo AS Pais_sede, COUNT(Codigo) AS Numero_de_aparicoes
 FROM Paises_em_alta
 WHERE Codigo IS NOT NULL
 GROUP BY Codigo
 UNION
 SELECT NULL AS Pais_sede, COUNT(*) AS Numero_de_aparicoes
 FROM Paises_em_alta
 WHERE Codigo IS NULL)
ORDER BY Numero_de_aparicoes DESC;

/*
>> Vídeos que já estiveram Em Alta de um canal
Exibe todos os vídeos e suas informações, em sua versão mais recente, de um dado canal que já estiveram em alta no nosso conjunto de dados.
*/
SET @Canal_buscado = 'MrBeast'; -- Nome do canal como entrada
SELECT V.ID,
	   VS.Titulo,
       CT.Nome AS Categoria,
       VS.Descricao,
       V.Data_de_publicacao,
       VS.Numero_de_likes,
       VS.Numero_de_comentarios,
       VS.Numero_de_visualizacoes,
       UAV.Ultima_data AS Ultima_vez_no_Trend
FROM Video AS V JOIN
		Video_Snapshot AS VS ON V.ID = VS.Video_ID JOIN
			Ultima_aparicao_video AS UAV ON V.ID = UAV.Video_ID AND
											VS.Data = UAV.Ultima_data JOIN
				Categoria AS CT ON V.Categoria_ID = CT.ID JOIN
						Canal_Snapshot AS CS USING (Canal_ID, Data)
WHERE CS.Titulo = @Canal_buscado
ORDER BY Ultima_vez_no_Trend DESC;

/*
>> Contar as categorias dos vídeos em alta de um canal
Mostra quantos vídeos de um certo canal estiveram em alta por categoria.
*/
SET @Canal_buscado = 'MrBeast'; -- Nome do canal como entrada
SELECT CT.Nome, COUNT(CT.Nome) AS Numero_de_videos
FROM Video AS V JOIN
		Video_Snapshot AS VS ON V.ID = VS.Video_ID JOIN
			Ultima_aparicao_video AS UAV ON VS.Video_ID = UAV.Video_ID AND
											VS.Data = UAV.Ultima_data JOIN
				Categoria AS CT ON V.Categoria_ID = CT.ID JOIN
					Canal_Snapshot AS CS USING (Canal_ID, Data)
WHERE CS.Titulo = @Canal_buscado
GROUP BY CT.Nome
ORDER BY Numero_de_videos DESC;

/*
>> Aparições das categorias no Em Alta
Mostra quantas vezes cada categoria apareceu no Em Alta. Consideramos como aparição cada ocorrência da categoria em um vídeo em sua última versão que esteve em alta em cada país do conjunto de dados.
*/
SELECT CT.Nome AS Categoria, COUNT(CT.Nome) AS Numero_de_aparicoes
FROM Ultima_aparicao_video_pais AS UAVP JOIN
		Video AS V ON UAVP.Video_ID = V.ID JOIN
			Categoria AS CT ON V.Categoria_ID = CT.ID
GROUP BY CT.Nome
ORDER BY Numero_de_aparicoes DESC;

/*
>> Total de visualizações por categoria no Em Alta
Mostra o total de visualizações dos vídeos em seu último estado no Em Alta por categoria.
*/
SELECT CT.Nome AS Categoria, SUM(VS.Numero_de_visualizacoes) AS Total_de_visualizacoes
FROM Ultima_aparicao_video AS UAV JOIN
		Video AS V ON UAV.Video_ID = V.ID JOIN
			Categoria AS CT ON V.Categoria_ID = CT.ID JOIN
				Video_Snapshot AS VS ON V.ID = VS.Video_ID AND
										UAV.Ultima_data = VS.Data
GROUP BY CT.Nome
ORDER BY Total_de_visualizacoes DESC;

/*
>> Total de curtidas por categoria no Em Alta
Mostra o total de likes dos vídeos em seu último estado no Em Alta por categoria.
*/
SELECT CT.Nome AS Categoria, SUM(VS.Numero_de_likes) AS Total_de_likes
FROM Ultima_aparicao_video AS UAV JOIN
		Video AS V ON UAV.Video_ID = V.ID JOIN
			Categoria AS CT ON V.Categoria_ID = CT.ID JOIN
				Video_Snapshot AS VS ON V.ID = VS.Video_ID AND
										UAV.Ultima_data = VS.Data
GROUP BY CT.Nome
ORDER BY Total_de_likes DESC;

/*
>> Tags com mais visualizações totais por categoria
Apresenta o total de visualizações que assuntos angariaram dentro de uma categoria a partir das tags dos vídeos em alta.
*/
SET @Categoria_buscada = 'Gaming'; -- Nome da categoria como entrada
SELECT T.Tag, SUM(VS.Numero_de_visualizacoes) AS Total_de_visualizacoes
FROM Ultima_aparicao_video AS UAV JOIN
		Video AS V ON UAV.Video_ID = V.ID JOIN
			Categoria AS CT ON V.Categoria_ID = CT.ID JOIN
				Video_Snapshot AS VS ON UAV.Video_ID = VS.Video_ID AND
										UAV.Ultima_data = VS.Data JOIN
					Tag AS T ON VS.Video_ID = T.Video_ID AND
								VS.Data = T.Video_Snapshot_Data
WHERE CT.Nome = @Categoria_buscada
GROUP BY T.Tag
ORDER BY Total_de_visualizacoes DESC;

/*
>> Países que um canal mais apareceu no Em Alta
Exibe os países que um canal apareceu mais vezes no Em Alta. Consideramos como aparição cada ocorrência de um vídeo do canal no Em Alta do país em uma data.
*/
SET @Canal_buscado = 'MrBeast'; -- Nome do canal como entrada
SELECT T.Pais_Codigo AS Pais, COUNT(CS.Titulo) AS Numero_de_vezes_no_Trend
FROM Canal_Snapshot AS CS JOIN
		Video AS V USING (Canal_ID) JOIN
			Video_Snapshot AS VS ON V.ID = VS.Video_ID AND
									CS.Data = VS.Data JOIN
				Trend AS T ON V.ID = T.Video_ID AND
							  VS.Data = T.Video_Snapshot_Data
WHERE CS.Titulo = @Canal_buscado
GROUP BY T.Pais_Codigo
ORDER BY Numero_de_vezes_no_Trend DESC;
