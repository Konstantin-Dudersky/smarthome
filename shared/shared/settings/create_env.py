"""Экспорт настроек в файл."""

import logging
from pathlib import Path
from typing import Any, Iterable

from dotenv import (
    get_key,  # pyright: ignore[reportUnknownVariableType]
    set_key,  # pyright: ignore[reportUnknownVariableType]
)

from .const import ENCODING
from .schema import Profiles, SettingsSchema

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def check_item_in_profile(
    key: str,
    profiles: Iterable[Profiles],
) -> bool:
    """Проверяет, есть в ключе key профиль profile.

    Если нет поля profiles, возвращает True

    Parameters
    ----------
    key: str
        ключ для проверки
    profiles: set[Prof]
        профили для проверки

    Returns
    -------
    True - можно экспортировать
    """
    schema_item: dict[str, Any] = SettingsSchema.schema()["properties"][key]
    if "profiles" not in schema_item.keys():
        return True
    return bool(set(profiles) & set(schema_item["profiles"]))


class CreateEnv(object):
    """Экспорт настроек в файл."""

    def __init__(
        self,
        profiles: Iterable[Profiles],
        env_file: Path,
    ) -> None:
        """Экспорт настроек в файл."""
        self.__profiles = profiles
        self.__env_file = env_file

    def export(self) -> None:
        """Выполнить экспорт."""
        log.info(
            "Экспортируем настройки для профилей: {0}".format(
                [profile.name for profile in self.__profiles],
            ),
        )
        log.debug("Записываем настройки:")
        for key, setting_default in SettingsSchema.construct().dict().items():
            self.__export_setting(key, setting_default)
        log.info(
            "Настройки сохранены в файле:\n{env_file}".format(
                env_file=self.__env_file,
            ),
        )

    def __export_setting(self, key: str, setting_default: Any):
        if not check_item_in_profile(key, self.__profiles):
            return
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
