"""Скрипты для выполнения из виртуального окружения."""

from pathlib import Path

from shared import SettingsProfiles, SettingsStore, Logger

Logger(output_to_console=True)


def create_env():
    """Создать файл с настройками."""
    SettingsStore("../.env").create_env(
        profiles={
            SettingsProfiles.api,
            SettingsProfiles.deconz_hub,
            SettingsProfiles.driver_deconz,
            SettingsProfiles.db,
            SettingsProfiles.pgadmin,
        },
    )


def export_env_schema() -> None:
    """Экспортировать схему настроек."""
    SettingsStore("../.env").export_schema(Path("../docs").resolve())
