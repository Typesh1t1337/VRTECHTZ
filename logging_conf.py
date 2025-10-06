import logging
import os
import sys
from pythonjsonlogger import jsonlogger


def setup_logging(log_file: str = "app_log.json"):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, log_file)
    log_handler = logging.FileHandler(log_path, encoding='utf-8', mode="a")
    formatter = jsonlogger.JsonFormatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    )
    log_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.handlers = []
    root_logger.addHandler(log_handler)
    root_logger.setLevel(logging.DEBUG)

    sa_logger = logging.getLogger('sqlalchemy.engine')
    sa_logger.setLevel(logging.INFO)
    sa_logger.propagate = True

    alembic_logger = logging.getLogger('alembic')
    alembic_logger.setLevel(logging.INFO)
    alembic_logger.propagate = True


