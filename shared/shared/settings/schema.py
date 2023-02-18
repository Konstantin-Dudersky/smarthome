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
from typing import Annotated

from pydantic import BaseSettings, EmailStr, Field, SecretStr

from .const import ENCODING

log: logging.Logger = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class SettingsSchema(BaseSettings):
    """Модель для сохранения настроек."""

    class Config(BaseSettings.Config):
        """Настройки."""

        env_file_encoding: str = ENCODING

    debug: bool = False
    timezone: str = Field(default="Europe/Minsk")

    db_user: Annotated[str, Field()] = "postgres"
    db_password: Annotated[SecretStr, Field()] = SecretStr("postgres")
    db_host: Annotated[ipaddress.IPv4Address, Field()] = ipaddress.IPv4Address(
        "192.168.101.10",
    )
    db_port: Annotated[int, Field()] = 5432

    driver_deconz_host: Annotated[
        ipaddress.IPv4Address, Field()
    ] = ipaddress.IPv4Address("192.168.101.10")
    driver_deconz_port: Annotated[int, Field()] = 8012

    deconz_hub_api_key: Annotated[SecretStr, Field()] = SecretStr("API_KEY")
    deconz_hub_host: Annotated[
        ipaddress.IPv4Address, Field()
    ] = ipaddress.IPv4Address("192.168.101.10")
    deconz_hub_port_api: Annotated[int, Field()] = 8010
    deconz_hub_port_vnc: Annotated[int, Field()] = 5901
    deconz_hub_port_ws: Annotated[int, Field()] = 8011
    deconz_hub_vnc_password: Annotated[SecretStr, Field()] = SecretStr(
        "password"
    )

    pgadmin_email: Annotated[EmailStr, Field()] = EmailStr("test@mail.com")
    pgadmin_password: Annotated[SecretStr, Field()] = SecretStr("password")
    pgadmin_port: Annotated[int, Field()] = 8080

    redis_port: Annotated[int, Field()] = 6379
