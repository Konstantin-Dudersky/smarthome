"""Sensors/switches in deconz."""

from asyncio import sleep as asleep

import httpx

from src.base.logic import CyclicRun
from src.base.types import SigBase, SigBool, Qual
from src.utils.logger import LoggerLevel, get_logger

from . import api, deconz, models

log = get_logger(__name__, LoggerLevel.INFO)


class BaseSensor:
    """Базовый класс для датчиков."""

    def __init__(
        self: "BaseSensor",
        resource_id: int,
        ws: deconz.Websocket,
    ) -> None:
        """Базовый класс для датчиков.

        :param resource_id: id сенсора
        :param ws: Канал сообщений websocket
        """
        self._id = resource_id
        self._ws = ws
        self._data: list[SigBase] = []
        self.__cyclic_run = CyclicRun(5.0)

    async def task(self: "BaseSensor") -> None:
        """Run task."""
        while True:
            await self._task()

    async def _task(self: "BaseSensor") -> None:
        if self.__cyclic_run():
            await self._update()
        # проверка сообщений websocket
        msg = self._ws.get_msg_general(self._id)
        if msg is not None:
            log.debug(
                "%s: в очереди новое сообщение: %s",
                repr(self),
                msg.attr,
            )
            await self._update()

    async def _update(self: "BaseSensor") -> None:
        raise NotImplementedError("Метод не переопределен.")

    async def _api_get_sensor(self: "BaseSensor") -> httpx.Response | None:
        msg = await api.get_sensor(self._id)
        if msg is None:
            log.warning(
                "%s, неудачная попытка обновить данные датчика",
                repr(self),
            )
            for item in self._data:
                item.qual = Qual.BAD
            return await asleep(0)
        log.debug("%s, обновление данных: %s", repr(self), msg.json())
        return await asleep(0, msg)

    def __repr__(self: "BaseSensor") -> str:
        """Represent string.

        :return: string representaion
        """
        return f"Deconz sensor id={self._id}"


class OpenClose(BaseSensor):
    """ZHAOpenClose."""

    def __init__(
        self: "OpenClose",
        resource_id: int,
        ws: deconz.Websocket,
    ) -> None:
        """Create open/close sensor.

        :param resource_id: id сенсора
        :param ws: Канал сообщений websocket
        """
        super().__init__(resource_id, ws)
        self.__data_opened = SigBool(False, Qual.BAD)
        # данные
        self._data.extend(
            [
                self.__data_opened,
            ],
        )

    async def opened(self: "OpenClose", update: bool = False) -> SigBool:
        """Состояние - открыт или закрыт.

        :param update: True - опрос, False - из памяти
        :return: состояние датчика
        """
        if update:
            await self._update()
        return await asleep(0, self.__data_opened)

    async def _task(self: "OpenClose") -> None:
        await super()._task()
        # проверка сообщений websocket
        msg = self._ws.get_msg_open_close(self._id)
        if msg is not None:
            log.debug(
                "%s: в очереди новое сообщение: %s",
                repr(self),
                msg.state.opened,
            )
            self.__data_opened.update(msg.state.opened, Qual.GOOD)
        return await asleep(0)

    async def _update(self: "OpenClose") -> None:
        """Принудительно обновить данные.

        :return: none
        """
        msg = await self._api_get_sensor()
        if msg is None:
            return await asleep(0)
        data = models.SensorOpenClose.parse_obj(msg.json())
        self.__data_opened.update(data.state.opened, Qual.GOOD)
        return await asleep(0)
