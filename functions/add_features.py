import pandas as pd
import re
import numpy as np

def add_features(df):
    df['word_count'] = df['text'].apply(lambda x: len(re.findall(r"\w+", x)), )
    df['character_count'] = df['text'].apply(lambda x: len(x))
    df['average_word_length'] = round(df['character_count']/df['word_count'].replace(0, np.nan), 2)
    df["title_word_count"] = df['title'].apply(lambda x: len(re.findall(r'\w+', x)))
    df["title_character_count"] = df['title'].apply(lambda x: len(x))
    df["exclamation_count"] = df['text'].apply(lambda x: x.count('!'))
    df['uppercase_ratio'] = df['text'].apply(lambda x: (sum(1 for ch in x if ch.isupper()) / sum(1 for ch in x if ch.isalpha())) if any(ch.isalpha() for ch in x) else 0)
    df['url_count'] = df['text'].apply(lambda x: len(re.findall(r'https?|ftp', x)))

    return df