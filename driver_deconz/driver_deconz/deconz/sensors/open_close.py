"""ZHAOpenClose."""

import datetime as dt

from .base_sensor import (
    BaseSensor,
    BaseSensorConfigModel,
    BaseSensorStateModel,
    BaseSensorModel,
)


class ZHAOpenCloseConfig(BaseSensorConfigModel):
    """ZHAOpenClose - конфигурация."""

    battery: int = 0
    on: bool = False
    reachable: bool = False
    temperature: int = 0


class ZHAOpenCloseState(BaseSensorStateModel):
    """ZHAOpenClose - состояние."""

    open: bool = False
    lowbattery: bool | None
    tampered: bool | None


class ZHAOpenClose(BaseSensorModel):
    """ZHAOpenClose."""

    config: ZHAOpenCloseConfig = ZHAOpenCloseConfig.construct()
    ep: int = 0
    lastannounced: dt.datetime = dt.datetime.min
    lastseen: dt.datetime = dt.datetime.min
    state: ZHAOpenCloseState = ZHAOpenCloseState.construct()


class OpenClose(BaseSensor[ZHAOpenClose]):
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
            model=ZHAOpenClose,
            model_state=ZHAOpenCloseState,
        )
