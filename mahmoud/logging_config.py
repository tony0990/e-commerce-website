import logging
import os


def setup_logging():
    if not os.path.exists("logs"):
        os.makedirs("logs")

    log_format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    log_level = logging.INFO

    logger = logging.getLogger("ecommerce")
    logger.setLevel(log_level)

    if logger.hasHandlers():
        return

    file_handler = logging.FileHandler("logs/app.log")
    file_handler.setFormatter(logging.Formatter(log_format))

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(log_format))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)