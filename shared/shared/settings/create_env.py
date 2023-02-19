"""Экспорт настроек в файл."""

import logging
from pathlib import Path
from typing import Any

from dotenv import get_key, set_key

from .const import ENCODING
from .schema import SettingsSchema

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class CreateEnv(object):
    """Экспорт настроек в файл."""

    def __init__(
        self,
        env_file: Path,
    ) -> None:
        """Экспорт настроек в файл."""
        self.__env_file = env_file

    def export(self) -> None:
        """Выполнить экспорт."""
        log.info("Экспортируем настройки".format())
        log.debug("Записываем настройки:")
        for key, setting_default in SettingsSchema.construct().dict().items():
            self.__export_setting(key, setting_default)
        log.info(
            "Настройки сохранены в файле:\n{env_file}".format(
                env_file=self.__env_file,
            ),
        )

    def __export_setting(self, key: str, setting_default: Any):
        setting_actual: str | None = get_key(
            dotenv_path=self.__env_file,
            key_to_get=key,
            encoding=ENCODING,
        )
        if setting_actual is not None:
            return
        set_key(
            dotenv_path=self.__env_file,
            key_to_set=key,
            value_to_set=setting_default,
            quote_mode="never",
            export=False,
            encoding=ENCODING,
        )
        log.debug("{0} = {1}".format(key, setting_default))
