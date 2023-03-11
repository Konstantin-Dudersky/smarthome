"""ZHATemperature."""

import datetime as dt

from shared import messages

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

    temperature: int = 0


class Model(BaseSensorModel):
    """Модель всех данных датчика."""

    config: ConfigModel = ConfigModel.construct()
    ep: int = 0
    lastannounced: dt.datetime | None = dt.datetime.min
    lastseen: dt.datetime = dt.datetime.min
    state: StateModel = StateModel.construct()


class Temperature(BaseSensor[Model]):
    """Датчик температуры."""

    def __init__(
        self,
        uniqueid: str,
        name: str,
    ) -> None:
        """Датчик температуры."""
        super().__init__(
            uniqueid=uniqueid,
            name=name,
            model=Model,
            model_state=StateModel,
        )

    def create_messages(self) -> None:
        """Создать сообщения для передачи в брокер."""
        self.messagebus.append(
            messages.TemperatureSensor(
                entity_id=self.name,
                temperature=self._data.state.temperature / 100.0,
                ts=self._data.state.lastupdated or dt.datetime.min,
            ).json(),
        )
