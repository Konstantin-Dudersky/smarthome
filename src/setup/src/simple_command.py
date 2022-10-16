"""Выполнить команду в указанной папке."""

import logging
import os
from typing import Callable

from ._shared import get_logger

log = get_logger(__name__, logging.DEBUG)


def execute(command: str) -> Callable[[], None]:
    """Выполнить команду в папке.

    :param command: команда
    :return: функция
    """

    def _main() -> None:
        log.info("-> Выполняем команду: %s", command)
        os.system(command)

    return _main
