import pandas as pd
import time, unicodedata

def remove_acentos(texto):
  texto = str(texto)
  if texto == 'nan':
    return ''
  return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')

def create_df(file_path):
  df = pd.read_csv(file_path)
  df['channel_country'].fillna('N/A', inplace=True)
  #print(df['channel_country'])
  trending_country = file_path[9:11]
  trending_country_col = [trending_country for i in range(df.shape[0])]
  #df['channel_country'] = df['channel_country'].str.replace('N/A', 'NULL')
  df['trending_country'] = trending_country_col
  df['trending_date'] = ("20" + df['trending_date']).str.replace('.', '-')
  df['trending_date'] = pd.to_datetime(df['trending_date'], format='%Y-%d-%m', errors='coerce').dt.strftime('%Y-%m-%d')
  df['publishedAt'] = (df['publishedAt'].str.replace('T', ' ')).str.replace('Z', '').str[0:10]
  df['channel_creation_date'] = (df['publishedAt'].str.replace('T', ' ')).str.replace('Z', '').str[0:10]
  return df
  
def csv_video_table(file_path, df):
  video = df[['video_id', 'channelId', 'publishedAt', 'categoryId']]
  video.columns = ['ID', 'Canal_ID', 'Data_hora_de_publicacao', 'Categoria_ID']
  video.to_csv(f'{file_path}/{date}_video.csv', index=False)
  return

def csv_canal_table(file_path, df):
  canal = df[['channelId', 'channel_creation_date']]
  canal = canal.drop_duplicates(subset='channelId')
  canal.columns = ['ID', 'Data_de_criacao']
  canal.to_csv(f'{file_path}/{date}_canal.csv', index=False)
  return

def csv_video_snapshot_table(file_path, df):
  video_snapshot = df[['title', 'likes', 'view_count', 'description', 'comment_count', 'trending_date', 'video_id']]
  video_snapshot.columns = ['Titulo', 'Numero_de_likes', 'Numero_de_visualizacoes', 'Descricao', 'Numero_de_comentarios', 'Data', 'Video_ID']
  video_snapshot.to_csv(f'{file_path}/{date}_video_snapshot.csv', index=False)
  return

def csv_canal_snapshot_table(file_path, df):
  canal_snapshot = df[['channelTitle', 'channel_video_count', 'channel_description', 'channel_image', 'channel_total_views', 
                       'channel_url', 'channel_subscriber_count', 'trending_date', 'channelId', 'channel_country']]
  canal_snapshot = canal_snapshot.drop_duplicates(subset='channelId')
  canal_snapshot.columns = ['Titulo', 'Numero_de_videos', 'Descricao', 'Imagem_de_perfil', 'Numero_de_visualizacoes',
                            'Link', 'Numero_de_inscritos', 'Data', 'Canal_ID', 'Pais_codigo']
  canal_snapshot.to_csv(f'{file_path}/{date}_canal_snapshot.csv', index=False)
  return

def csv_trend_table(file_path, df):
  trend = pd.DataFrame()
  trend['Pais_Codigo'] = df['trending_country']
  trend[['Video_ID', 'Video_Snapshot_Data']] = df[['video_id', 'trending_date']]
  trend.to_csv(f'{file_path}/{date}_trend.csv', index=False)
  return

def csv_pais_table(file_path, df):
  pais = df[['channel_country']]
  #pais = pais[pais['channel_country'] != 'NULL']
  #pais = pais[pais['channel_country'].notna() & (pais['channel_country'] != '')]
  pais = pais.drop_duplicates()
  pais.columns = ['Codigo']
  pais.to_csv(f'{file_path}/{date}_pais.csv', index=False)
  return

def csv_tag_table(file_path, df):
  tag = df[['video_id', 'tags', 'trending_date']]
  tag['tags'] = tag['tags'].str.split(',')
  tag = tag.explode('tags')
  tag.columns = ['Video_ID', 'Tag', 'Video_Snapshot_Data']
  tag['Tag'] = tag['Tag'].str.strip().str.lower()
  tag['Tag'] = tag['Tag'].apply(remove_acentos)
  tag = tag.drop_duplicates()
  tag.to_csv(f'{file_path}/{date}_tag.csv', index=False)
  return

def csv_palavras_chave_table(file_path, df):
    palavras_chave = df[['channelId', 'channel_keywords', 'trending_date']]
    palavras_chave['channel_keywords'] = palavras_chave['channel_keywords'].str.split(' ')
    palavras_chave = palavras_chave.explode('channel_keywords')
    palavras_chave.columns = ['Canal_ID', 'Palavra_chave', 'Canal_Snapshot_Data']

    # Padroniza as strings na coluna Palavra_chave
    palavras_chave['Palavra_chave'] = palavras_chave['Palavra_chave'].str.strip().str.lower()
    palavras_chave['Palavra_chave'] = palavras_chave['Palavra_chave'].apply(remove_acentos)

    palavras_chave = palavras_chave.drop_duplicates()
    palavras_chave.to_csv(f'{file_path}/{date}_palavra_chave.csv', index=False)
    return

def generate_tables(file_path, df):
  csv_video_table(file_path, df)
  csv_canal_table(file_path, df)
  csv_canal_snapshot_table(file_path, df)
  csv_video_snapshot_table(file_path, df)
  csv_tag_table(file_path, df)
  csv_palavras_chave_table(file_path, df)
  csv_trend_table(file_path, df)
  csv_pais_table(file_path, df)
  return

date = '24.25.10'
# date = time.strftime('%y.%d.%m')

df = create_df(f'{date}_BR_videos.csv')
generate_tables('treated_tables', df)