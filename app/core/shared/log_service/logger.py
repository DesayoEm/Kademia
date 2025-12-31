import logging
import os
from logging.handlers import TimedRotatingFileHandler


def general_logging():
    if not os.path.exists("logs"):
        os.makedirs("logs")

    logger = logging.getLogger("kademia")
    logger.setLevel(logging.INFO)

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            },
            "detailed": {
                "format": "[%(levelname)s|%(module)s|L%(lineno)d] %(asctime)s: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "json": {
                "()": "logger.JSONFormatter",
                "fmt_keys": {
                    "level": "levelname",
                    "message": "message",
                    "timestamp": "timestamp",
                    "logger": "name",
                    "module": "module",
                    "function": "function",
                    "line": "lineno",
                },
            },
        },
        "handlers": {
            "main_file": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": "logs/main.log",
                "when": "midnight",
                "maxBytes": 10_000_000,
                "backupCount": 30,
                "level": "DEBUG",
                "formatter": "json",
            },
            "error_file": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": "logs/errors.log",
                "when": "midnight",
                "maxBytes": 5_000_000,
                "backupCount": 30,
                "level": "ERROR",
                "formatter": "json",
            },
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "json",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "uvicorn.access": {
                "handlers": ["main_file", "error_file"],
                "level": "WARNING",
                "propagate": True,
            },
            "sqlalchemy.engine": {
                "handlers": ["main_file", "error_file"],
                "level": "WARNING",
                "propagate": True,
            },
        },
        "root": {"handlers": ["main_file", "error_file"], "level": "DEBUG"},
    }

    return logger


def auth_logging():
    if not os.path.exists("auth_logs"):
        os.makedirs("auth_logs")

    auth_logger = logging.getLogger("kademia.security")
    auth_logger.setLevel(logging.INFO)

    if not auth_logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        file_handler = TimedRotatingFileHandler(
            filename="auth_logs/app.log",
            when="midnight",
            interval=1,
            backupCount=7,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)

        auth_logger.addHandler(stream_handler)
        auth_logger.addHandler(file_handler)

    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    return auth_logger


logger = general_logging()
auth_logger = auth_logging()
