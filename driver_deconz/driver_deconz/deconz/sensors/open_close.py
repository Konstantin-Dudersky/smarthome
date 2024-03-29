"""ZHAOpenClose."""

import datetime as dt

from shared.messages import messages

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
    lastannounced: dt.datetime | None = None
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
        self.messagebus.append(
            messages.OpenCloseSensor(
                entity_id=self.name,
                opened=self._data.state.open,
                ts=self._data.state.lastupdated or dt.datetime.min,
            ).json(),
        )
