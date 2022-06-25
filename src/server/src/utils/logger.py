"""Setup logging.

in files:

from src.utils.logger import LoggerLevel, get_logger
logger = get_logger(__name__, LoggerLevel.INFO)
"""

import logging
import os
import socket
from enum import IntEnum
from logging import handlers

FORMAT = (
    "%(levelname)s: %(asctime)s | "
    "%(name)s:%(lineno)d - %(funcName)s | "
    "\n⮡ %(message)s"
)

# ------------------------------------------------------------------------------


class CustomFormatter(logging.Formatter):
    """Custom formatter."""

    GREEN = "\x1b[32;20m"
    GREY = "\x1b[38;20m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    BOLD_RED = "\x1b[31;1m"
    RESET = "\x1b[0m"

    def get_format(self: "CustomFormatter", text: str, levelno: int) -> str:
        """Цвет сообщения.

        :param text: текст, цвет которого нужно изменить
        :param levelno: класс сообщения
        :return: текст с измененным текстом
        """
        match levelno:
            case logging.DEBUG:
                return self.GREY + text + self.RESET
            case logging.INFO:
                return self.GREEN + text + self.RESET
            case logging.DEBUG:
                return self.YELLOW + text + self.RESET
            case logging.ERROR:
                return self.RED + text + self.RESET
            case logging.CRITICAL:
                return self.BOLD_RED + text + self.RESET
        return text

    def format(self: "CustomFormatter", record: logging.LogRecord) -> str:
        """Format function.

        :param record: запись логгера
        :return: отформатированная запись логгера
        """
        log_fmt = self.get_format(FORMAT, record.levelno)
        formatter = logging.Formatter(log_fmt)
        return (
            formatter.format(record)
            + "\n"
            + self.get_format("-" * 80, record.levelno)
        )


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


def get_logger(
    name: str,
    level: LoggerLevel = LoggerLevel.INFO,
) -> logging.Logger:
    """Return logger with name.

    :param name: название логгера
    :param level: уровень логгирования
    :return: объект логгера
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger


# ------------------------------------------------------------------------------


_logger = get_logger(__name__)
_logger.info("Start at host: %s", socket.gethostname())
