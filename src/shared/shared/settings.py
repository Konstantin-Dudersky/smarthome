"""Настройки приложения.

Для создания файла с дефолтными настройками запустить функцию create_env():

- создаем задачу poe:

[tool.poe.tasks.create_env]
help = "Создание файла с настройками"
script = "src.shared.settings:create_env"

- запускаем:

poetry run poe create_env

Для чтения настроек импортировать:

from src.shared.settings import SettingsSchema, settings_store
settings: SettingsSchema = settings_store.settings
"""

import ipaddress
import logging
import os
from enum import Enum
from typing import Annotated, Any

from dotenv import (
    get_key,  # pyright: ignore[reportUnknownVariableType]
    set_key,  # pyright: ignore[reportUnknownVariableType]
)
from pydantic import BaseSettings, Field, EmailStr, SecretStr
from typing_extensions import Self

log: logging.Logger = logging.getLogger(__name__)
log.setLevel(logging.INFO)

ENV_FILE: str = ".env"
ENCODING: str = "utf-8"


class Prof(Enum):
    """Профили настроек."""

    api = "api"
    dev = "dev"
    driver_ascue = "driver_ascue"
    deconz_hub = "deconz_hub"
    db = "db"
    pgadmin = "pgadmin"


class SettingsSchema(BaseSettings):
    """Модель для сохранения настроек."""

    class Config(BaseSettings.Config):
        """Настройки."""

        env_file: str = ENV_FILE
        env_file_encoding: str = ENCODING

    debug: bool = False
    timezone: str = Field(default="Europe/Minsk")

    db_user: Annotated[str, Field(profiles=[Prof.db])] = "postgres"
    db_password: Annotated[
        SecretStr,
        Field(profiles=[Prof.db]),
    ] = SecretStr("postgres")
    db_host: Annotated[
        ipaddress.IPv4Address, Field(profiles=[Prof.db])
    ] = ipaddress.IPv4Address("192.168.101.11")
    db_port: Annotated[int, Field(profiles=[Prof.db])] = 5432

    deconz_hub_host: Annotated[
        ipaddress.IPv4Address, Field(profiles=[Prof.deconz_hub])
    ] = ipaddress.IPv4Address("192.168.101.11")
    deconz_hub_port_api: Annotated[
        int, Field(profiles=[Prof.deconz_hub])
    ] = 8001
    deconz_hub_port_vnc: Annotated[
        int, Field(profiles=[Prof.deconz_hub])
    ] = 5901

    pgadmin_email: Annotated[
        EmailStr, Field(profiles=[Prof.pgadmin])
    ] = EmailStr("test@mail.com")
    pgadmin_password: Annotated[
        SecretStr, Field(profiles=[Prof.pgadmin])
    ] = SecretStr("password")
    pgadmin_port: Annotated[int, Field(profiles=[Prof.pgadmin])] = 8080


def check_item_in_profile(
    key: str,
    profiles: set[Prof],
) -> bool:
    """Проверяет, есть в ключе key профиль profile.

    Если нет поля profiles, возвращает True

    :param key: ключ для проверки
    :param profiles: профили для проверки
    :return: True - можно экспортировать
    """
    schema_item: dict[str, Any] = SettingsSchema.schema()["properties"][key]
    if "profiles" not in schema_item.keys():
        return False
    return bool(profiles & set(schema_item["profiles"]))


def create_env(profiles: set[Prof]) -> None:
    """Записывает файл с дефолтными значениями.

    Экспортируются настройки,
    у которых в поле profiles указан необходимый профиль.
    Если у настройки нето поля profiles, она всегда экспортируется.

    :param profiles: профили для экспорта настроек.
    """
    print(  # noqa: WPS421
        "Экспортируем настройки для профилей: ",
        [profile.name for profile in profiles],
    )
    print("\nНастройки:\n")  # noqa: WPS421
    for key, setting_default in SettingsSchema.construct().dict().items():
        if not check_item_in_profile(key, profiles):
            continue
        setting_actual: str | None = get_key(
            dotenv_path=ENV_FILE,
            key_to_get=key,
            encoding=ENCODING,
        )
        if setting_actual is None:
            set_key(
                dotenv_path=ENV_FILE,
                key_to_set=key,
                value_to_set=setting_default,
                quote_mode="never",
                export=False,
                encoding=ENCODING,
            )
            print(f"{key} = {setting_default}")  # noqa: WPS421
        else:
            print(f"{key} = {setting_actual}")  # noqa: WPS421
    print(  # noqa: WPS421
        f"\nНастройки сохранены в файле:\n\n{os.getcwd()}/{ENV_FILE}",
    )


class SettingsStore(object):
    """Хранение настроек."""

    __settings: SettingsSchema | None

    def __init__(self: Self) -> None:
        """Хранение настроек."""
        self.__settings = None

    @property
    def settings(self: Self) -> SettingsSchema:
        """Получить настройки.

        :return: настройки
        """
        if self.__settings is None:
            self.__settings = SettingsSchema()
            print("Settings:", self.__settings.json())  # noqa: WPS421
        return self.__settings


def export_env(path: str, filename: str) -> None:
    """Экспортировать настройки в формате JSON.

    :param path: папка для экспорта
    :param filename: название файла для экспорта
    """
    with open(
        f"{path}/{filename}.schema.json",
        "w",
        encoding="utf-8",
    ) as export_schema:
        export_schema.write(SettingsSchema().schema_json())
    with open(
        f"{path}/{filename}.values.json",
        "w",
        encoding="utf-8",
    ) as export_values:
        export_values.write(SettingsSchema().json())


settings_store: SettingsStore = SettingsStore()
