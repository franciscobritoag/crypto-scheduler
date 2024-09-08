import logging

def setup_logging():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    print(f"Logger level set to: {logging.getLevelName(logger.level)}")
    return logger
