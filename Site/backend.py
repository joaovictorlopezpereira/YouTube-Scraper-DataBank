from flask import Flask, request, render_template, send_file
import mysql.connector
import matplotlib.pyplot as plt
import io

#opções do select mapeadas para suas respectivas querys no SQL
consultas = {
    "consulta1":  
''' 
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
''',
     "consulta2":
'''
SELECT V.ID, 
       VS.Titulo, 
       CS.Titulo AS Canal,
       CT.Nome AS Categoria, 
       VS.Descricao,
       V.Data_de_publicacao, 
       VS.Numero_de_likes, 
       VS.Numero_de_comentarios,
       VS.Numero_de_visualizacoes
FROM Video AS V JOIN
        Video_Snapshot AS VS ON V.ID = VS.Video_ID JOIN
            Categoria AS CT ON V.Categoria_ID = CT.ID JOIN
                Trend AS T ON VS.Video_ID = T.Video_ID AND
                              VS.Data = T.Video_Snapshot_Data JOIN
                    Canal_Snapshot AS CS USING (Canal_ID, Data)
WHERE VS.Data = @Data_buscada AND T.Pais_Codigo = @Pais_buscado
ORDER BY VS.Numero_de_visualizacoes DESC;
''',
     "consulta3":
'''
SELECT Palavra_chave, COUNT(Palavra_chave) AS Numero_de_usos
FROM Ultima_aparicao_canal_pais AS UACP JOIN
        Palavra_chave AS PC ON UACP.Canal_ID = PC.Canal_ID AND
                               UACP.Ultima_data = PC.Canal_Snapshot_Data
GROUP BY Palavra_chave
ORDER BY Numero_de_usos DESC;
''',
     "consulta4": 
'''
SELECT Tag, COUNT(Tag) AS Numero_de_usos
FROM Ultima_aparicao_video_pais AS UAVP JOIN
        Tag AS T ON UAVP.Video_ID = T.Video_ID AND
                    UAVP.Ultima_data = T.Video_Snapshot_Data
GROUP BY Tag
ORDER BY Numero_de_usos DESC;
''',
     "consulta5": #SOMAR STRING COM SET!
'''
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
''',
     "consulta6":
'''
SELECT CT.Nome AS Categoria, SUM(VS.Numero_de_visualizacoes) AS Total_de_visualizacoes
FROM Ultima_aparicao_video AS UAV JOIN
        Video AS V ON UAV.Video_ID = V.ID JOIN
            Categoria AS CT ON V.Categoria_ID = CT.ID JOIN
                Video_Snapshot AS VS ON V.ID = VS.Video_ID AND
                                        UAV.Ultima_data = VS.Data
GROUP BY CT.Nome
ORDER BY Total_de_visualizacoes DESC;
''',
     "consulta7":
'''
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
''',
     "consulta8": 
'''
SELECT CT.Nome AS Categoria, SUM(VS.Numero_de_likes) AS Total_de_likes
FROM Ultima_aparicao_video AS UAV JOIN
        Video AS V ON UAV.Video_ID = V.ID JOIN
            Categoria AS CT ON V.Categoria_ID = CT.ID JOIN
                Video_Snapshot AS VS ON V.ID = VS.Video_ID AND
                                        UAV.Ultima_data = VS.Data
GROUP BY CT.Nome
ORDER BY Total_de_likes DESC;
''',
     "consulta9":
'''
SELECT CT.Nome AS Categoria, COUNT(CT.Nome) AS Numero_de_aparicoes
FROM Ultima_aparicao_video_pais AS UAVP JOIN
        Video AS V ON UAVP.Video_ID = V.ID JOIN
            Categoria AS CT ON V.Categoria_ID = CT.ID
GROUP BY CT.Nome
ORDER BY Numero_de_aparicoes DESC;
''',
     "consulta10": #SOMAR COM SET
'''
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
''',
     "consulta11": #SOMAR COM SET
'''
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
''',
     "consulta12":
'''
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
''',
     "consulta13":
'''
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
''',
     "consulta14":
'''
SELECT C.ID,
       CS.Titulo,
       CS.Descricao,
       C.Data_de_criacao,
       CS.Pais_Codigo AS Pais_sede,
       CS.Numero_de_inscritos,
       CS.Numero_de_videos,
       CS.Numero_de_visualizacoes,
       UAC.Ultima_data AS Ultima_vez_no_Trend
FROM Ultima_aparicao_canal AS UAC JOIN
        Canal AS C ON UAC.Canal_ID = C.ID JOIN
            Canal_Snapshot AS CS ON C.ID = CS.Canal_ID AND
                                    UAC.Ultima_data = CS.Data
ORDER BY Numero_de_inscritos DESC;
'''
}

#opções do select mapeadas para seus respectivos nomes
nome_tabela = {
     "consulta1": "Vídeos em alta de um canal",
     "consulta2": "Vídeos em alta em um país",
     "consulta3": "Palavras chaves mais utilizadas",
     "consulta4": "Tags mais utilizadas",
     "consulta5": "Tags com mais visualizações",
     "consulta6": "Views por categoria",
     "consulta7": "Views por canal",
     "consulta8": "Likes por categoria",
     "consulta9": "Aparições em alta por categoria",
     "consulta10": "Categorias dos vídeos em alta por canal",
     "consulta11": "Aparições de um canal por país",
     "consulta12": "Aparições de países no em alta",
     "consulta13": "Aparições no em alta por canal",
     "consulta14": "Canais que já apareceram no em alta"
}

app = Flask(__name__)

#configurações iniciais para funcionamento do banco de dados
db_config = {
    'host': 'localhost',       #Substitua pelo endereço do seu servidor MySQL
    'user': 'root',     #Substitua pelo seu usuário MySQL
    'password': 'YuTeJh321',   #Substitua pela sua senha MySQL
    'database': 'youtube'      #Substitua pelo nome do banco de dados
}

global_xs = None
global_ys = None
global_tabela = None
plt.switch_backend('agg')

#usa a variável global da tabela para separar os valores em duas listas, que se tornam eixos do gráfico a ser plotado
def faz_eixos():
     eixo_x = list(global_tabela[0].keys())[0][0:25]
     eixo_y = list(global_tabela[0].keys())[1][0:25]
     xs = [element[eixo_x] for element in global_tabela]
     ys = [element[eixo_y] for element in global_tabela]
     return xs, ys

#envia o gráfico gerado no python para a página html
@app.route('/grafico')
def gera_grafico():
     buf = faz_grafico()
     return send_file(buf, mimetype='image/png')

#usa os eixos feitos pela função faz_eixos() para construir o gráfico da tabela em questão
def faz_grafico():
     xs, ys = faz_eixos()
     plt.figure(figsize=(20, 15)) 
     plt.barh(xs, ys)
     plt.title(f'{list(global_tabela[0].keys())[0]} x {list(global_tabela[0].keys())[1]}')
     plt.xlabel(list(global_tabela[0].keys())[1])
     plt.ylabel(list(global_tabela[0].keys())[0])
     plt.legend()
     buf = io.BytesIO()
     plt.savefig(buf, format='png')
     buf.seek(0)
     plt.close()
     return buf

#renderiza a página do menu
@app.route('/')
def index():
     return render_template("index.html")

#filtra a consulta apropriada através do input do usuário e então gera o gráfico, se houver
@app.route('/consultas', methods=['POST'])
def processar():
     try:
          dado = request.form['consultas']
          filtro1 = request.form["filtro1"]
          consulta = consultas[dado]
          conn = mysql.connector.connect(**db_config)
          cursor = conn.cursor(dictionary=True)
          if dado == 'consulta2':
               cursor.execute(f'SET @Data_buscada = "{filtro1}";')
               cursor.execute(f'SET @Pais_buscado = "{request.form["filtro2"]}";')
          elif dado == 'consulta1' or dado == 'consulta10' or dado == 'consulta11':
               cursor.execute(f'SET @Canal_buscado = "{filtro1}";')
          elif dado == 'consulta5':
               cursor.execute(f'SET @Categoria_buscada = "{filtro1}";')
          consulta = consulta[0:len(consulta) - 2] + ' LIMIT 50;'
          print(consulta)
          cursor.execute(consulta)
          tabela = cursor.fetchall()
          cursor.close()
          conn.close()
          if dado in ['consulta3', 'consulta4', 'consulta5', 'consulta6', 'consulta7', 'consulta8', 'consulta9', 'consulta10', 'consulta11', 'consulta13']:
               global global_tabela
               global_tabela = tabela
               gera_grafico()
          return render_template('tabela.html', tabela=tabela, consulta=dado, nome_tabela=nome_tabela[dado])
     except:
          return render_template('tabela.html', tabela=[{}], consulta='', nome_tabela='')
     
if __name__ == "__main__":
  app.run()
