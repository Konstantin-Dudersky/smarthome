"""Скрипты для выполнения из виртуального окружения."""

import os
from pathlib import Path

from shared import settings


def create_env():
    path_str = "{current}/..".format(current=os.getcwd())
    path = Path(path_str).resolve()
    settings.create_env(
        work_dir_abs=path,
        profiles={settings.Prof.deconz_hub},
    )
