"""Файл для настроек.

Для чтения настроек импортировать:
from src.utils.settings import settings

Для создания файла с дефолтными настройками запустить функцию create_env():
poetry run poe create_env
"""

# ошибка в set_key
# pyright: reportUnknownVariableType=false
# ошибка наследования Config
# pyright: reportIncompatibleVariableOverride=false

from typing import TYPE_CHECKING

from dotenv import set_key

from pydantic import BaseSettings

if TYPE_CHECKING:
    IPvAnyAddress = str
else:
    from pydantic import IPvAnyAddress

ENV_FILE = ".env"
ENCODING = "utf-8"


class Settings(BaseSettings):
    """Модель для сохранения настроек."""

    class Config:
        """Настройки."""

        env_file = ENV_FILE
        env_file_encoding = ENCODING

    debug: bool = False
    deconz_ip: IPvAnyAddress = "192.168.101.10"
    deconz_rest_port: int = 80
    deconz_api_key: str = "303E2AD17F"
    db_url: str = "sqlite:///db.sqlite3"
    telegram_token: str = "5422079866:AAFarQ9FrwDRj08k73e5JB-e9eSag020iqQ"
    telegram_chat_id: str = "-1001555100085"
    yeelight_bathroom: IPvAnyAddress = "192.168.101.20"


def create_env() -> None:
    """Записывает файл с дефолтными значениями."""
    # создает файл или очищает, если уже был
    for key, value in Settings().dict().items():
        set_key(
            dotenv_path=ENV_FILE,
            key_to_set=key,
            value_to_set=value,
            quote_mode="never",
            export=False,
            encoding="utf-8",
        )


settings = Settings()

if __name__ == "__main__":
    pass
