"""ZHALightLevel."""

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
    tholddark: int = 0
    tholdoffset: int = 0


class StateModel(BaseSensorStateModel):
    """Модель состояния."""

    dark: bool = False
    daylight: bool = False
    lightlevel: int = 0
    lux: int = 0


class Model(BaseSensorModel):
    """Модель всех данных датчика."""

    config: ConfigModel = ConfigModel.construct()
    ep: int = 0
    lastannounced: dt.datetime | None = None
    lastseen: dt.datetime = dt.datetime.min
    state: StateModel = StateModel.construct()


class LightLevel(BaseSensor[Model]):
    """Датчик освещенности."""

    def __init__(
        self,
        uniqueid: str,
        name: str,
    ) -> None:
        """Датчик освещенности."""
        super().__init__(
            uniqueid=uniqueid,
            name=name,
            model=Model,
            model_state=StateModel,
        )

    def create_messages(self) -> None:
        """Создать сообщения для передачи в брокер."""
        self.messagebus.append(
            messages.LightLevel(
                entity_id=self.name,
                lux=self._data.state.lux,
                ts=self._data.state.lastupdated or dt.datetime.min,
            ).json(),
        )
