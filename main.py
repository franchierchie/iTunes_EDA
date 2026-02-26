import logging

from src.config.logging import setup_logging
from src.extract.read_source import extract_data
from src.transform.transform_data import clean_data
from src.load.load_data import load_data

logger = logging.getLogger(__name__)

if __name__ == '__main__':
  setup_logging()
  logger.info("ETL Pipeline started")

  df = extract_data()
  logger.info("Extract completed: %d rows", len(df))

  clean_df = clean_data(df)
  logger.info("Transform completed")

  load_data(clean_df)
  logger.info("Load completed")