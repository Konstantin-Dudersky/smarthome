"""Setup logging.

in files:
    from src.utils.logger import LoggerLevel, get_logger
    logger = get_logger(__name__)
    logger.setLevel(LoggerLevel.INFO)
"""

import logging
import os
import socket
from enum import IntEnum
from logging import handlers

FORMAT_PART1 = "%(levelname)s: %(asctime)s | "
FORMAT_PART2 = "%(name)s:%(lineno)d - %(funcName)s | "
FORMAT_PART3 = "%(message)s"
FORMAT = FORMAT_PART1 + FORMAT_PART2 + FORMAT_PART3


# ------------------------------------------------------------------------------


class CustomFormatter(logging.Formatter):
    """Custom formatter."""

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    FORMATS = {
        logging.DEBUG: grey + FORMAT + reset,
        logging.INFO: grey + FORMAT + reset,
        logging.WARNING: yellow + FORMAT + reset,
        logging.ERROR: red + FORMAT + reset,
        logging.CRITICAL: bold_red + FORMAT + reset,
    }

    def format(self: "CustomFormatter", record: logging.LogRecord) -> str:
        """Format function."""
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


# ------------------------------------------------------------------------------


class LoggerLevel(IntEnum):
    """Logging levels."""

    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    NOTSET = logging.NOTSET


# ------------------------------------------------------------------------------


os.makedirs("logs", exist_ok=True)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(CustomFormatter())

logging.basicConfig(
    format=FORMAT,
    level=logging.INFO,
    handlers=[
        handlers.RotatingFileHandler(
            filename="logs/log.log",
            mode="a",
            maxBytes=5 * 1024 * 1024,
            backupCount=2,
            encoding=None,
            delay=False,
        ),
        stream_handler,
    ],
)


def get_logger(name: str) -> logging.Logger:
    """Return logger with name."""
    return logging.getLogger(name)


# ------------------------------------------------------------------------------


_logger = get_logger(__name__)
_logger.info("--------------------------------------------------")
_logger.info("Start at host: %s", socket.gethostname())
