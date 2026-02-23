import logging

from src.config.logging import setup_logging

logger = logging.getLogger(__name__)

if __name__ == '__main__':
  setup_logging()
  logger.info("ETL Pipeline started")

  # logger.info("Extract completed: %d rows", len(df))

  # logger.info("Transform completed")

  # logger.info("Load completed")