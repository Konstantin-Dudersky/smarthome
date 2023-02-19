"""Daylight."""

import datetime as dt

from .base_sensor import (
    BaseSensor,
    BaseSensorConfigModel,
    BaseSensorStateModel,
    BaseSensorModel,
)


class ConfigModel(BaseSensorConfigModel):
    """Модель конфигурации."""

    configured: bool = False
    on: bool = False
    sunriseoffset: int = 0
    sunsetoffset: int = 0


class StateModel(BaseSensorStateModel):
    """Модель состояния."""

    open: bool = False
    lowbattery: bool | None
    tampered: bool | None

    dark: bool = False
    daylight: bool = False
    lastupdated: dt.datetime = dt.datetime.min
    status: int = 0
    sunrise: dt.datetime = dt.datetime.min
    sunset: dt.datetime = dt.datetime.min


class Model(BaseSensorModel):
    """Модель всех данных датчика."""

    config: ConfigModel = ConfigModel.construct()
    ep: int = 0
    lastannounced: dt.datetime = dt.datetime.min
    lastseen: dt.datetime = dt.datetime.min
    state: StateModel = StateModel.construct()


class Daylight(BaseSensor[Model]):
    """Программный датчик времени суток."""

    def __init__(
        self,
        uniqueid: str,
        name: str,
    ) -> None:
        """Программный датчик времени суток."""
        super().__init__(
            uniqueid=uniqueid,
            name=name,
            model=Model,
            model_state=StateModel,
        )

    def create_messages(self) -> None:
        """Создать сообщения для передачи в брокер."""
        pass
