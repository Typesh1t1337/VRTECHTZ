import logging
import os
from pythonjsonlogger import jsonlogger


def get_logger():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
    log_dir = "logs"
    new_log_dir = os.path.join(parent_dir, log_dir)
    os.makedirs(new_log_dir, exist_ok=True)
    log_path = os.path.join(new_log_dir, "celery_log.json")

    logger = logging.getLogger("update_logger")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        formatter = jsonlogger.JsonFormatter(fmt="%(asctime)s %(levelname)s %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
