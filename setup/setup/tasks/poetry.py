"""Установка poetry."""

import logging
import os
from typing import Callable


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


# obsolete ---------------------------------------------------------------------


def poetry_self_install(version: str = "1.1.14") -> Callable[[], None]:
    """Entry point."""

    def _main() -> None:
        os.system("sudo apt update")
        os.system("sudo apt install -y python3-venv curl")
        os.system(
            "curl -sSL https://install.python-poetry.org"
            f" | python3 - --version {version}"
        )
        print(
            """-> Если следующая команда выполняется с ошибкой
-> Command 'poetry' not found
-> нужно добавить в файл .bashrc
-> export PATH="$HOME/.local/bin:$PATH"
"""
        )
        os.system(". ~/.profile && poetry config virtualenvs.in-project true")

    return _main


def poetry_self_update(version: str = "1.1.14") -> Callable[[], None]:
    """Entry point."""

    def _main() -> None:
        os.system(f"poetry self update {version}")

    return _main
