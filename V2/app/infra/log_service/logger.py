import logging
import os
from logging.handlers import TimedRotatingFileHandler

def general_logging():
    if not os.path.exists('logs'):
        os.makedirs('logs')

    logger = logging.getLogger('kademia')
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        file_handler = TimedRotatingFileHandler(
            filename='logs/app.log',
            when='midnight',
            interval=1,
            backupCount=7,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)

        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)

    logging.getLogger('uvicorn.access').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

    return logger


def auth_logging():
    if not os.path.exists('auth_logs'):
        os.makedirs('auth_logs')

    auth_logger = logging.getLogger('kademia.security')
    auth_logger.setLevel(logging.INFO)

    if not auth_logger.handlers:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        file_handler = TimedRotatingFileHandler(
            filename='auth_logs/app.log',
            when='midnight',
            interval=1,
            backupCount=7,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)

        auth_logger.addHandler(stream_handler)
        auth_logger.addHandler(file_handler)

    logging.getLogger('uvicorn.access').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

    return auth_logger

logger = general_logging()
auth_logger = auth_logging()


