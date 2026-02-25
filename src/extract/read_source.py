import pandas as pd

from src.config.settings import RAW_DATA

def extract_data() -> pd.DataFrame:
  df = pd.read_csv(RAW_DATA)
  return df