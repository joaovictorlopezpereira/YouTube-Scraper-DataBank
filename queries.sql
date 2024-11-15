/* 
>> Quantidade de views em alta por canal
Exibe, em ordem decrescente de total de visualizações, os canais que mais tiveram
visualizações em seus vídeos em alta durante o período de coleta.
*/
WITH
	Video_mais_recente AS
		(SELECT V.ID, V.Canal_ID, VS.Numero_de_visualizacoes
         FROM (SELECT V.ID, MAX(VS.Data) AS Ultima_data
			   FROM Video AS V JOIN
					Video_Snapshot AS VS ON V.ID = VS.Video_ID
			   GROUP BY V.ID) AS UDA JOIN
					Video AS V ON UDA.ID = V.ID JOIN
						Video_Snapshot AS VS ON V.ID = VS.Video_ID AND
																		UDA.Ultima_data = VS.Data)
SELECT DISTINCT CS.Titulo AS Canal, VR.Total_de_visualizacoes
FROM (SELECT Canal_ID, SUM(Numero_de_visualizacoes) AS Total_de_visualizacoes
	  FROM Video_mais_recente
    	GROUP BY Canal_ID) AS VR JOIN
		Canal_Snapshot AS CS USING (Canal_ID)
ORDER BY VR.Total_de_visualizacoes DESC;

/*
>> Canais que ficaram no em alta mais vezes
Exibe, em ordem decrescente, os canais que mais apareceram no Em Alta e a quantidade
de vezes que isso aconteceu. Consideramos como aparição cada ocorrência de um vídeo do
canal no Em Alta de um país em uma data.
*/
SELECT CS.Titulo AS Canal, COUNT(CS.Canal_ID) AS Numero_de_vezes_no_Trend
FROM Trend AS T JOIN
		Video_Snapshot AS VS ON T.Video_ID = VS.Video_ID AND
														T.Video_Snapshot_Data = VS.Data JOIN
			Video AS V ON VS.Video_ID = V.ID JOIN
				Canal AS C ON V.Canal_ID = C.ID JOIN
					Canal_Snapshot AS CS ON C.ID = CS.Canal_ID AND
																	VS.Data = CS.Data
GROUP BY CS.Titulo
ORDER BY Numero_de_vezes_no_Trend DESC;

/*
>> Tags mais utilizadas
Exibe, em ordem descrescente, o número de vezes que uma tag apareceu em algum
vídeo em alta. Consideramos como aparição cada ocorrência de uma tag em um vídeo
no Em Alta de um país em uma data. 
*/
SELECT Tag, COUNT(Tag) AS Numero_de_usos
FROM (SELECT Video_ID, MAX(Video_Snapshot_Data) AS Ultima_data
	  FROM Tag
      GROUP BY Video_ID) AS VMR JOIN
		Tag AS T ON VMR.Video_ID = T.Video_ID AND
															 VMR.Ultima_data = T.Video_Snapshot_Data
GROUP BY Tag
ORDER BY Numero_de_usos DESC;

/*
>> Palavras-chave mais utilizadas
Exibe, em ordem descrescente, o número de vezes que uma palavra-chave apareceu em
algum vídeo em alta. Consideramos como aparição cada ocorrência de uma palavra-chave
em um canal para cada vídeo seu no Em Alta de um país em uma data. 
*/
SELECT Palavra_chave, COUNT(Palavra_chave) AS Numero_de_usos
FROM (SELECT Canal_ID, MAX(Canal_Snapshot_Data) AS Ultima_data
	  FROM Palavra_chave
      GROUP BY Canal_ID) AS CMR JOIN
		Palavra_chave AS PC ON CMR.Canal_ID = PC.Canal_ID AND
							   					 CMR.Ultima_data = PC.Canal_Snapshot_Data
GROUP BY Palavra_chave
ORDER BY Numero_de_usos DESC;

/*
>> Países (ou não) que mais apareceram no Em Alta
Apresenta cada país e o número de vezes que um canal sediado apareceu no Em Alta.
Consideramos como aparição cada ocorrência de canal sediado no país para cada
vídeo seu no Em Alta de um país em uma data.
*/
WITH
	Paises_em_alta AS
		(SELECT P.Codigo, C.ID
         FROM Canal_Snapshot AS CS LEFT JOIN
				Pais AS P ON CS.Pais_Codigo = P.Codigo JOIN
					Canal AS C ON CS.Canal_ID = C.ID JOIN
						Video AS V ON C.ID = V.Canal_ID JOIN
							Video_Snapshot AS VS ON V.ID = VS.Video_ID AND
																			CS.Data = VS.Data)
(SELECT Codigo AS Pais_sede, COUNT(Codigo) AS Numero_de_aparicoes
 FROM Paises_em_alta
 WHERE Codigo IS NOT NULL
 GROUP BY Codigo
 UNION
 SELECT NULL AS Pais_sede, COUNT(*) AS Numero_de_aparicoes
 FROM Paises_em_alta
 WHERE Codigo IS NULL)
ORDER BY Numero_de_aparicoes DESC;