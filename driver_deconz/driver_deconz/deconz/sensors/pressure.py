"""ZHAPressure."""

import datetime as dt

from .base_sensor import (
    BaseSensor,
    BaseSensorConfigModel,
    BaseSensorStateModel,
    BaseSensorModel,
)


class ConfigModel(BaseSensorConfigModel):
    """Модель конфигурации."""

    battery: int = 0
    on: bool = False
    reachable: bool = False
    offset: int = 0


class StateModel(BaseSensorStateModel):
    """Модель состояния.."""

    pressure: int = 0


class Model(BaseSensorModel):
    """Модель всех данных датчика."""

    config: ConfigModel = ConfigModel.construct()
    ep: int = 0
    lastannounced: dt.datetime | None = dt.datetime.min
    lastseen: dt.datetime = dt.datetime.min
    state: StateModel = StateModel.construct()


class Pressure(BaseSensor[Model]):
    """Датчик давления."""

    def __init__(
        self,
        uniqueid: str,
        name: str,
    ) -> None:
        """Датчик давления."""
        super().__init__(
            uniqueid=uniqueid,
            name=name,
            model=Model,
            model_state=StateModel,
        )