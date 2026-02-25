import logging

from src.config.logging import setup_logging
from src.extract.read_source import extract_data
from src.transform.transform_data import clean_data

logger = logging.getLogger(__name__)

if __name__ == '__main__':
  setup_logging()
  logger.info("ETL Pipeline started")

  df = extract_data()
  logger.info("Extract completed: %d rows", len(df))

  clean_df = clean_data(df)
  # descriptive_analysis()
  # logger.info("Transform completed")

  # logger.info("Load completed")