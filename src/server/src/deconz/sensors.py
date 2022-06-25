"""Sensors/switches in deconz."""

import asyncio
from asyncio import sleep as asleep
import time

from src.utils.logger import LoggerLevel, get_logger

from . import api, deconz, models

logger = get_logger(__name__, LoggerLevel.DEBUG)


class CyclicRun:
    """Циклическое выполнение."""

    def __init__(self: "CyclicRun", time_between: float = 1.0) -> None:
        """Циклическое выполнение.

        :param time_between: Время между вызовами, [s]
        """
        self.__last_call = 0
        self.__time_between = int(time_between * 1e9)
        self.__started = False

    @property
    def run(self: "CyclicRun") -> bool:
        """Проверка, что время истекло.

        Нужно циклически вызывать.

        :return: True - время истекло
        """
        self.__started = True
        now = time.perf_counter_ns()
        if (now - self.__last_call) > self.__time_between:
            self.__last_call = now
            return True
        return False

    @property
    def started(self: "CyclicRun") -> bool:
        """Запускалась ли функция run хотя бы раз.

        :return: True - функция run выполнялась
        """
        return self.__started


class OpenClose:
    """ZHAOpenClose."""

    def __init__(
        self: "OpenClose",
        sensor_id: int,
        ws: deconz.Websocket,
    ) -> None:
        """Create open/close sensor.

        :param sensor_id: id сенсора TODO откуда
        :param ws: Канал сообщений websocket
        """
        self.__id = sensor_id
        self.__data: models.SensorOpenClose | None = None
        self.__ws = ws
        self.__cyclic_run = CyclicRun(300.0)

    async def opened(self: "OpenClose", update: bool = False) -> bool | None:
        """Состояние - открыт или закрыт.

        :param update: True - опрос, False - из памяти
        :return: состояние датчика
        """
        if update:
            await self._update()
        if self.__data is None:
            return await asleep(0)
        return await asleep(0, self.__data.state.opened)

    async def run(self: "OpenClose") -> None:
        """Run task."""
        while True:
            await self.__run()

    async def __run(self: "OpenClose") -> None:
        if self.__cyclic_run.run:
            await self._update()
        # проверка сообщений websocket
        msg = self.__ws.get_msg_open_close(self.__id)
        if msg is not None:
            logger.debug(
                "%s: в очереди новое сообщение: %s",
                repr(self),
                msg.state.opened,
            )
            if self.__data is not None:
                self.__data.state.opened = msg.state.opened
                self.__data.state.lastupdated = msg.state.lastupdated
        msg2 = self.__ws.get_msg_general(self.__id)
        if msg2 is not None:
            logger.debug(
                "%s: в очереди новое сообщение: %s",
                repr(self),
                msg2.attr,
            )
            await self._update()
        return await asyncio.sleep(0)

    async def _update(self: "OpenClose") -> models.SensorOpenClose | None:
        """Принудительно обновить данные.

        :return: Возвращает полученные данные или None
        """
        data = await api.get_sensor(self.__id)
        if data is None:
            logger.warning(
                "%s, неудачная попытка обновить данные датчика",
                repr(self),
            )
            return await asleep(0)
        logger.debug("%s, обновление данных: %s", repr(self), data.json())
        self.__data = models.SensorOpenClose.parse_obj(data.json())
        return await asleep(0, result=self.__data)

    def __repr__(self: "OpenClose") -> str:
        """Represent string.

        :return: string representaion
        """
        return f"Deconz sensor id={self.__id}"
