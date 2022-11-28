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
from enum import Enum
from typing import Annotated

from pydantic import BaseSettings, EmailStr, Field, SecretStr

from .const import ENCODING

log: logging.Logger = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class Profiles(Enum):
    """Профили настроек."""

    api = "api"
    deconz_hub = "deconz_hub"
    driver_deconz = "driver_deconz"
    db = "db"
    pgadmin = "pgadmin"


class SettingsSchema(BaseSettings):
    """Модель для сохранения настроек."""

    class Config(BaseSettings.Config):
        """Настройки."""

        env_file_encoding: str = ENCODING

    debug: bool = False
    timezone: str = Field(default="Europe/Minsk")

    db_user: Annotated[str, Field(profiles=[Profiles.db])] = "postgres"
    db_password: Annotated[
        SecretStr,
        Field(profiles=[Profiles.db]),
    ] = SecretStr("postgres")
    db_host: Annotated[
        ipaddress.IPv4Address,
        Field(profiles=[Profiles.db]),
    ] = ipaddress.IPv4Address("192.168.101.10")
    db_port: Annotated[int, Field(profiles=[Profiles.db])] = 5432

    driver_deconz_host: Annotated[
        ipaddress.IPv4Address,
        Field(profiles=[Profiles.driver_deconz]),
    ] = ipaddress.IPv4Address("192.168.101.10")
    driver_deconz_port: Annotated[
        int,
        Field(profiles=[Profiles.driver_deconz]),
    ] = 8012

    deconz_hub_api_key: Annotated[
        SecretStr,
        Field(profiles=[Profiles.deconz_hub]),
    ] = SecretStr("API_KEY")
    deconz_hub_host: Annotated[
        ipaddress.IPv4Address,
        Field(profiles=[Profiles.deconz_hub]),
    ] = ipaddress.IPv4Address("192.168.101.10")
    deconz_hub_port_api: Annotated[
        int,
        Field(profiles=[Profiles.deconz_hub]),
    ] = 8010
    deconz_hub_port_vnc: Annotated[
        int,
        Field(profiles=[Profiles.deconz_hub]),
    ] = 5901
    deconz_hub_port_ws: Annotated[
        int,
        Field(profiles=[Profiles.deconz_hub]),
    ] = 8011
    deconz_hub_vnc_password: Annotated[
        SecretStr,
        Field(profiles=[Profiles.deconz_hub]),
    ] = SecretStr("password")

    pgadmin_email: Annotated[
        EmailStr,
        Field(profiles=[Profiles.pgadmin]),
    ] = EmailStr("test@mail.com")
    pgadmin_password: Annotated[
        SecretStr,
        Field(profiles=[Profiles.pgadmin]),
    ] = SecretStr("password")
    pgadmin_port: Annotated[int, Field(profiles=[Profiles.pgadmin])] = 8080
