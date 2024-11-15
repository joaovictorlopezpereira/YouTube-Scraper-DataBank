import pandas as pd
import os

def create_df(file_path, país):
  df = pd.read_csv(file_path)
  trending_country = país
  trending_country_col = [trending_country for i in range(df.shape[0])]
  df['trending_country'] = trending_country_col
  df['trending_date'] = ("20" + df['trending_date']).str.replace('.', '-')
  df['trending_date'] = pd.to_datetime(df['trending_date'], format='%Y-%d-%m', errors='coerce').dt.strftime('%Y-%m-%d')
  df['publishedAt'] = df['publishedAt'].str[0:10]
  df['channel_country'].fillna('ZZ', inplace=True)
  df['channel_creation_date'] = df['channel_creation_date'].str[0:10]
  return df
  
def csv_video_table(df, data, país):
  video = df[['video_id', 'channelId', 'publishedAt', 'categoryId']]
  video.columns = ['ID', 'Canal_ID', 'Data_hora_de_publicacao', 'Categoria_ID']
  video.to_csv(f'csvzinhos/{data}_{país}_video.csv', index=False)
  return;

def csv_canal_table(df, data, país):
  canal = df[['channelId', 'channel_creation_date']]
  canal.columns = ['ID', 'Data_de_criacao']
  canal.to_csv(f'csvzinhos/{data}_{país}_canal.csv', index=False)
  return;

def csv_pais_table(df, data, país):
  pais = df[['channel_country']]
  pais.columns = ['Codigo']
  pais = pais.drop_duplicates()
  pais = pais.dropna(how='all')
  pais = pais.dropna(how='any')
  pais.to_csv(f'csvzinhos/{data}_{país}_pais.csv', index=False)
  return

def csv_video_snapshot_table(df, data, país):
  video_snapshot = df[['title', 'likes', 'view_count', 'description', 'comment_count', 'trending_date', 'video_id']]
  video_snapshot.columns = ['Titulo', 'Numero_de_likes', 'Numero_de_visualizacoes', 'Descricao', 'Numero_de_comentarios', 'Data', 'Video_ID']
  video_snapshot.to_csv(f'csvzinhos/{data}_{país}_video_snapshot.csv', index=False)
  return;

def csv_canal_snapshot_table(df, data, país):
  canal_snapshot = df[['channelTitle', 'channel_video_count', 'channel_description', 'channel_image', 'channel_total_views', 
                       'channel_url', 'channel_subscriber_count', 'trending_date', 'channelId', 'channel_country']]
  canal_snapshot.columns = ['Titulo', 'Numero_de_videos', 'Descricao', 'Imagem_de_perfil', 'Numero_de_visualizacoes',
                            'Link', 'Numero_de_inscritos', 'Data', 'Canal_ID', 'Pais_codigo']
  canal_snapshot.to_csv(f'csvzinhos/{data}_{país}_canal_snapshot.csv', index=False)
  return;

def csv_tag_table(df, data, país):
  tag = df[['video_id', 'tags', 'trending_date']]
  tag['tags'] = tag['tags'].str.split(',')
  tag = tag.explode('tags')
  tag.columns = ['Video_ID', 'Tag', 'Video_Snapshot_Data']
  tag['Tag'] = tag['Tag'].str.strip()
  tag = df[df['Tag'] != '[none]']
  tag.to_csv(f'csvzinhos/{data}_{país}_tag.csv', index=False)
  return;

def csv_palavras_chave_table(df, data, país):
  palavras_chave = df[['channelId', 'channel_keywords', 'trending_date']]
  palavras_chave['channel_keywords'] = palavras_chave['channel_keywords'].str.split(' ')
  palavras_chave = palavras_chave.explode('channel_keywords')
  palavras_chave.columns = ['Channel_ID', 'Palavra_Chave', 'Trending_Date']
  palavras_chave['Palavra_Chave'] = palavras_chave['Palavra_Chave'].str.strip()
  palavras_chave = df[df['Palavra_Chave'] != '']
  palavras_chave.to_csv(f'csvzinhos/{data}_{país}_palavra_chave.csv', index=False)
  return;

def csv_trend_table(df, data, país):
  trend = pd.DataFrame()
  trend['Pais_Codigo'] = df['trending_country']
  trend[['Video_ID', 'Video_Snapshot_Data']] = df[['video_id', 'trending_date']]
  trend.to_csv(f'csvzinhos/{data}_{país}_trend.csv', index=False)
  return;

caminho_pasta = 'CSV_originais'
arquivos = [arquivo for arquivo in os.listdir(caminho_pasta) if os.path.isfile(os.path.join(caminho_pasta, arquivo))]
for arquivo in arquivos:
  data = arquivo[0:8]
  país = arquivo[9:11]
  df = create_df(f'{caminho_pasta}/{arquivo}', país)
  csv_video_table(df, data, país)
  csv_canal_table(df, data, país)
  csv_video_snapshot_table(df, data, país)
  csv_canal_snapshot_table(df, data, país)
  csv_tag_table(df, data, país)
  csv_palavras_chave_table(df, data, país)
  csv_trend_table(df, data, país)
  csv_pais_table(df, data, país)