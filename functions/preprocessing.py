import pandas as pd
from functions.add_features import add_features

def prepare_df(title, text):
    df = pd.DataFrame({"title":[title], "text":[text]})
    df['full_text'] = df['title'] + ' ' + df['text']
    df = add_features(df)
    df = df.drop(['title', 'text'], axis=1)
    return df