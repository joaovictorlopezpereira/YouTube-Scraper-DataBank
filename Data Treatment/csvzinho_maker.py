import pandas as pd

def create_df(file_path):
  df = pd.read_csv(file_path)
  trending_country = file_path[9:11]
  trending_country_col = [trending_country for i in range(df.shape[0])]
  df['trending_country'] = trending_country_col
  df['trending_date'] = ("20" + df['trending_date']).str.replace('.', '-')
  df['publishedAt'] = (df['publishedAt'].str.replace('T', ' ')).str.replace('Z', '')
  df['channel_creation_date'] = (df['publishedAt'].str.replace('T', ' ')).str.replace('Z', '')
  return df
  
def csv_video_table(df):
  video = df[['video_id', 'channelId', 'publishedAt', 'categoryId']]
  video.columns = ['ID', 'Canal_ID', 'Data_hora_de_publicacao', 'Categoria_ID']
  video.to_csv('csvzinhos/video.csv', index=False)
  return;

def csv_canal_table(df):
  canal = df[['channelId', 'channel_creation_date']]
  canal.columns = ['ID', 'Data_de_criacao']
  canal.to_csv('csvzinhos/canal.csv', index=False)
  return;

def csv_pais_table(df):
  pais = df[['channel_country']]
  pais = pais.drop_duplicates()
  pais.columns = ['Codigo']
  pais.to_csv('csvzinhos/pais.csv', index=False)
  return;

def csv_video_snapshot_table(df):
  video_snapshot = df[['title', 'likes', 'view_count', 'description', 'comment_count', 'trending_date', 'video_id']]
  video_snapshot.columns = ['Titulo', 'Numero_de_likes', 'Numero_de_visualizacoes', 'Descricao', 'Numero_de_comentarios', 'Data', 'Video_ID']
  video_snapshot.to_csv('csvzinhos/video_snapshot.csv', index=False)
  return;

def csv_canal_snapshot_table(df):
  canal_snapshot = df[['channelTitle', 'channel_video_count', 'channel_description', 'channel_image', 'channel_total_views', 
                       'channel_url', 'channel_subscriber_count', 'trending_date', 'channelId', 'channel_country']]
  canal_snapshot.columns = ['Titulo', 'Numero_de_videos', 'Descricao', 'Imagem_de_perfil', 'Numero_de_visualizacoes',
                            'Link', 'Numero_de_inscritos', 'Data', 'Canal_ID', 'Pais_codigo']
  canal_snapshot.to_csv('csvzinhos/canal_snapshot.csv', index=False)
  return;

def csv_tag_table(df):
  tag = df[['video_id', 'tags', 'trending_date']]
  tag['tags'] = tag['tags'].str.split(',')
  tag = tag.explode('tags')
  tag.columns = ['Video_ID', 'Tag', 'Video_Snapshot_Data']
  tag['Tag'] = tag['Tag'].str.strip()
  tag.to_csv('csvzinhos/tag.csv', index=False)
  return;

def csv_palavras_chave_table(df):
  palavras_chave = df[['channelId', 'channel_keywords', 'trending_date']]
  palavras_chave['channel_keywords'] = palavras_chave['channel_keywords'].str.split(' ')
  palavras_chave = palavras_chave.explode('channel_keywords')
  palavras_chave.columns = ['Channel_ID', 'Keyword', 'Trending_Date']
  palavras_chave['Keyword'] = palavras_chave['Keyword'].str.strip()
  palavras_chave.to_csv('csvzinhos/channel_keywords.csv', index=False)
  return;

def csv_trend_table(df):
  trend = pd.DataFrame()
  trend['Pais_Codigo'] = df['trending_country']
  trend[['Video_ID', 'Video_Snapshot_Data']] = df[['video_id', 'trending_date']]
  trend.to_csv('csvzinhos/trend.csv', index=False)
  return;


date = '24.25.10'
df = create_df(f'{date}_BR_videos.csv')
csv_video_table(df)
csv_canal_table(df)
csv_pais_table(df)
csv_video_snapshot_table(df)
csv_canal_snapshot_table(df)
csv_tag_table(df)
csv_palavras_chave_table(df)
csv_trend_table(df)
