"""ZHAOpenClose."""

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
    temperature: int = 0


class StateModel(BaseSensorStateModel):
    """Модель состояния."""

    open: bool = False
    lowbattery: bool | None
    tampered: bool | None


class Model(BaseSensorModel):
    """Модель всех данных датчика."""

    config: ConfigModel = ConfigModel.construct()
    ep: int = 0
    lastannounced: dt.datetime = dt.datetime.min
    lastseen: dt.datetime = dt.datetime.min
    state: StateModel = StateModel.construct()


class OpenClose(BaseSensor[Model]):
    """Датчик открытия / закрытия."""

    def __init__(
        self,
        uniqueid: str,
        name: str,
    ) -> None:
        """Датчик открытия / закрытия."""
        super().__init__(
            uniqueid=uniqueid,
            name=name,
            model=Model,
            model_state=StateModel,
        )

    def create_messages(self) -> None:
        """Создать сообщения для передачи в брокер."""
        self._messages.clear()
        self._messages.add(
            messages.BinarySensor(
                entity=self.name,
                opened=self._data.state.open,
            ).json(),
        )
