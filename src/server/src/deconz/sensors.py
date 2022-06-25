"""Sensors/switches in deconz."""

import asyncio
from enum import Enum, auto

from src.utils.logger import LoggerLevel, get_logger

from . import api, deconz, models

logger = get_logger(__name__)
logger.setLevel(LoggerLevel.DEBUG)


class SensorStates(Enum):
    """Состояния датчиков."""

    INIT = auto()
    CONNECTED = auto()


class OpenClose:
    """ZHAOpenClose."""

    def __init__(
        self: "OpenClose",
        sensor_id: int,
        ws: deconz.Websocket,
    ) -> None:
        """Create open/close sensor.

        :param sensor_id: id сенсора TODO
        :param ws: Канал сообщений websocket
        """
        self.__id = sensor_id
        self.__state = SensorStates.INIT
        self.__data: models.SensorOpenClose | None = None
        self.__ws = ws

    async def run(self: "OpenClose") -> None:
        """Run task."""
        while True:
            await self.__run()

    async def __run(self: "OpenClose") -> None:
        match self.__state:
            case SensorStates.INIT:
                data = await api.get_sensor(self.__id)
                if data is None:
                    await asyncio.sleep(5)
                    return
                self.__data = models.SensorOpenClose(**data.json())
                self.__state = SensorStates.CONNECTED
                logger.info("Датчик %s получил данные", self.__id)
                logger.debug(self.__data)

            case SensorStates.CONNECTED:
                msg = self.__ws.get_msg_open_close(self.__id)
                if msg is not None:
                    logger.debug(
                        "%s: в очереди новое сообщение: %s",
                        repr(self),
                        msg.state.opened,
                    )
                msg2 = self.__ws.get_msg_general(self.__id)
                if msg2 is not None:
                    logger.debug(
                        "%s: в очереди новое сообщение: %s",
                        repr(self),
                        msg2.attr,
                    )

        await asyncio.sleep(0)
