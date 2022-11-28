"""Singleton для управления настройками."""

import logging
from pathlib import Path
from typing import Final, Iterable

from shared.patterns import SingletonMeta

from .create_env import CreateEnv
from .schema import Profiles, SettingsSchema

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


MSG_READ: Final[str] = "Прочитаны настройки приложения:\n{settings}"

SCHEMA_JSON: Final[str] = "{path}/{env_file}.schema.json"
VALUES_JSON: Final[str] = "{path}/{env_file}.values.json"


class SettingsStore(object, metaclass=SingletonMeta["SettingsStore"]):
    """Класс для управления настройками."""

    def __init__(self, env_file: str = ".env") -> None:
        """Класс для управления настройками."""
        self.__env_file = Path(env_file).resolve()
        self.__settings = SettingsSchema(
            _env_file=env_file,  # pyright: ignore[reportGeneralTypeIssues]
        )
        log.debug(MSG_READ.format(settings=self.settings.dict()))

    @property
    def settings(self) -> SettingsSchema:
        """Настройки."""
        return self.__settings

    def create_env(
        self,
        profiles: Iterable[Profiles],
    ) -> None:
        """Записывает файл с дефолтными значениями.

        Экспортируются настройки,
        у которых в поле profiles указан необходимый профиль.
        Если у настройки нет поля profiles, она всегда экспортируется.

        Parameters
        ----------
        profiles
            профили для экспорта настроек
        """
        CreateEnv(
            profiles=profiles,
            env_file=self.__env_file,
        ).export()

    def export_schema(self, path: Path) -> None:
        """Экспортировать настройки в формате JSON.

        Parameters
        ----------
        path: Path
            папка для экспорта
        """
        env_file = str(self.__env_file.name).strip(".")
        with open(
            SCHEMA_JSON.format(
                path=path,
                env_file=env_file,
            ),
            "w",
            encoding="utf-8",
        ) as export_schema:
            export_schema.write(SettingsSchema.schema_json())
        with open(
            VALUES_JSON.format(
                path=path,
                env_file=env_file,
            ),
            "w",
            encoding="utf-8",
        ) as export_values:
            export_values.write(self.__settings.json())


if __name__ == "__main__":
    s1 = SettingsStore("../.env")
    s2 = SettingsStore.instance()
