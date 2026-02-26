
from src.config.settings import REPORTS_DIR_PATH

def load_data(clean_df) -> None:
  if clean_df.empty:
    raise ValueError("The DataFrame passed as an argument is empty")
  
  clean_df.to_csv(f'{REPORTS_DIR_PATH}/clean_df.csv')