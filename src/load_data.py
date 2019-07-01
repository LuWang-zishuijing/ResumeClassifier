import pandas as pd

def load_data(data1_path, data2_path):
    df_actors_name = pd.read_csv(data2_path, sep=',')
    df_actors_name.columns = ['actor_id', 'actor_name']
    df_words = pd.read_csv(data1_path, sep='\t')
    return pd.merge(df_actors_name, df_words, on="actor_id")