"""Скрипты для выполнения из виртуального окружения."""

from pathlib import Path

from shared import Logger
from shared.settings import SettingsStore

Logger(output_to_console=True)


def create_env():
    """Создать файл с настройками."""
    SettingsStore("../.env").create_env()


def export_env_schema() -> None:
    """Экспортировать схему настроек."""
    SettingsStore("../.env").export_schema(Path("../docs").resolve())
