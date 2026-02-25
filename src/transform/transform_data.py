import pandas as pd
import numpy as np
import warnings

from src.config.settings import REQUIRED_RAW_COLUMNS

def validate_input_schema(df: pd.DataFrame) -> None:
  missing = REQUIRED_RAW_COLUMNS - set(df.columns)
  if missing:
    raise ValueError(f"Missing required columns: {missing}")



def clean_data(df: pd.DataFrame):
  validate_input_schema(df)

  # print("_______________ HEAD _______________")
  # print(df.head())
  # print("_______________ SHAPE _______________")
  # print(df.shape)
  # print("_______________ COLUMNS _______________")
  # print(df.columns)
  # print("_______________ INFO _______________")
  # print(df.info())
  # print("_______________ DESCRIBE _______________")
  # print(df.describe())

  if df['track_id'].isna().any():
    raise ValueError("Null values found in track_id column")

  # Drop rows where artist_name is missing
  df = df.dropna(subset=['artist_name']).copy()


  # Standardise categoricals
  for col in ['genre', 'artist_name', 'track_name', 'collection_name']:
    df[col] = df[col].astype(str).str.strip()
  df['genre'] = df['genre'].str.title()
  df['artist_name'] = df['artist_name'].str.strip().str.title()


  # Rating --> is_explicit flag
  df['rating'].astype(str).str.strip().str.title()
  explicit_map = {'Explicit': True, 'Clean': False, 'Not Explicit': False, 'Notexplicit': False}
  df['is_explicit'] = df['rating'].map(explicit_map).fillna(False)


  # Price: clip negatives, then impute
  df['track_price']      = df['track_price'].clip(lower=0)
  df['collection_price'] = df['collection_price'].clip(lower=0)
  df['track_price']      = df.groupby('genre')['track_price'].transform(lambda x: x.fillna(x.median()))
  df['collection_price'] = df.groupby('genre')['collection_price'].transform(lambda x: x.fillna(x.median()))
  df['track_price']      = df['track_price'].fillna(df['track_price'].median())
  df['collection_price'] = df['collection_price'].fillna(df['collection_price'].median())


  # Duration flags
  df['duration_min_raw'] = df['track_time_millis'] / 60000
  df['duration_flag'] = df['duration_min_raw'].apply(
    lambda x: 'very_short' if x < 0.5 else ('very_long' if x > 60 else 'normal')
  )


  # Dates (album-median --> artist-median --> global-median imputation)
  df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
  df['release_date'] = df['release_date'].fillna(df.groupby('collection_name')['release_date'].transform('median'))
  df['release_date'] = df['release_date'].fillna(df.groupby('artist_name')['release_date'].transform('median'))
  df['release_date'] = df['release_date'].fillna(df['release_date'].median())
  df['release_date'] = df['release_date'].dt.tz_localize(None)


  # Features
  df['release_year'] = df['release_date'].dt.year.astype(int)
  df['duration_min'] = df['track_time_millis'] / 60000
  df['revenue_proxy'] = df['track_price']

  # Column renaming
  rename_map = {
    'track_name': 'track_title', 'collection_name': 'album_name',
    'track_price': 'unit_price', 'collection_price': 'album_price',
    'track_time_millis': 'duration_ms',
  }
  df.rename(columns=rename_map, inplace=True)
  
  # Drop unnecessary columns
  cols_to_drop = ['country', 'currency', 'rating', 'preview_url', 'artwork_url', 'album_artist']
  df = df.drop(columns=cols_to_drop)
  df.drop_duplicates(inplace=True)
  df.reset_index(drop=True, inplace=True)
  
  # print("_______________ HEAD _______________")
  # print(df.head())
  # print("_______________ SHAPE _______________")
  # print(df.shape)
  # print("_______________ COLUMNS _______________")
  # print(df.columns)
  # print("_______________ INFO _______________")
  # print(df.info())
  # print("_______________ DESCRIBE _______________")
  # print(df.describe())

  return df