"""Настройки приложения."""

import ipaddress
import logging

from pydantic import BaseSettings, EmailStr, Field, SecretStr

from .const import ENCODING

log: logging.Logger = logging.getLogger(__name__)
log.setLevel(logging.INFO)

DEFAULT_IP = ipaddress.IPv4Address("192.168.101.10")


class SettingsSchema(BaseSettings):
    """Модель для сохранения настроек."""

    class Config(BaseSettings.Config):
        """Настройки."""

        env_file_encoding: str = ENCODING

    debug: bool = False
    timezone: str = Field(default="Europe/Minsk")

    db_user: str = "postgres"
    db_password: SecretStr = SecretStr("postgres")
    db_host: ipaddress.IPv4Address = DEFAULT_IP
    db_port: int = 5432

    deconz_hub_api_key: SecretStr = SecretStr("API_KEY")
    deconz_hub_host: ipaddress.IPv4Address = DEFAULT_IP
    deconz_hub_port_api: int = 8010
    deconz_hub_port_vnc: int = 5901
    deconz_hub_port_ws: int = 8011
    deconz_hub_vnc_password: SecretStr = SecretStr("password")

    driver_deconz_host: ipaddress.IPv4Address = DEFAULT_IP
    driver_deconz_port: int = 8012

    grafana_port: int = 8013

    pgadmin_email: EmailStr = EmailStr("test@mail.com")
    pgadmin_password: SecretStr = SecretStr("password")
    pgadmin_port: int = 8080

    redis_host: ipaddress.IPv4Address = DEFAULT_IP
    redis_port: int = 6379
    redis_ui_port: int = 8014
