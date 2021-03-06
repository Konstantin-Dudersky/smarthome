"""Sensors/switches in deconz."""

from asyncio import sleep as asleep
from typing import Any, Coroutine

from typing_extensions import Self

import httpx

from pydantic import BaseModel

from src.base.logic import CyclicRun
from src.base.signals import SigBase, SigBool, SigFloat, Qual, Units
from src.utils.logger import LoggerLevel, get_logger

from . import api, deconz, schemas

log = get_logger(__name__, LoggerLevel.INFO)


class BaseSensor:
    """Базовый класс для датчиков."""

    class Schema(BaseModel):
        """Схема для API."""

        title: str

    def __init__(
        self: "BaseSensor",
        title: str,
        resource_id: int,
        update_rate: float,
        ws: deconz.Websocket,
    ) -> None:
        """Базовый класс для датчиков.

        :param title: название датчика
        :param resource_id: id сенсора
        :param ws: Канал сообщений websocket
        :param update_rate: период обновления датчика, [s]
        """
        self._id = resource_id
        self._ws = ws
        self._data: list[SigBase] = []
        self.__cyclic_run = CyclicRun(update_rate)
        self._title = title

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
                msg,
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

    class Schema(BaseSensor.Schema):
        """Схема для API."""

        opened: SigBool.Schema

    def __init__(
        self: "OpenClose",
        title: str,
        resource_id: int,
        ws: deconz.Websocket,
        atasks: list[Coroutine[Any, Any, None]],
        update_rate: float = 5.0,
    ) -> None:
        """Create open/close sensor.

        :param title: название датчика
        :param resource_id: id сенсора
        :param ws: Канал сообщений websocket
        :param atasks: Ссылка на список асинхронных задач
        :param update_rate: период обновления датчика, [s]
        """
        super().__init__(
            title=title,
            resource_id=resource_id,
            ws=ws,
            update_rate=update_rate,
        )
        self.__data_opened = SigBool()
        # данные
        self._data.extend(
            [
                self.__data_opened,
            ],
        )
        atasks.append(self.task())

    @property
    def schema(self: "OpenClose") -> Schema:
        """Схема для API.

        :return: схема для API
        """
        return self.Schema(
            title=self._title,
            opened=self.__data_opened.schema,
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
        data = schemas.ZHAOpenClose.parse_obj(msg.json())
        self.__data_opened.update(data.state.opened, Qual.GOOD)
        return await asleep(0)


class Presence(BaseSensor):
    """ZHAPresence."""

    def __init__(
        self: "Presence",
        title: str,
        resource_id: int,
        ws: deconz.Websocket,
        atasks: list[Coroutine[Any, Any, None]],
        update_rate: float = 5.0,
    ) -> None:
        """Create open/close sensor.

        :param title: название датчика
        :param resource_id: id сенсора
        :param ws: Канал сообщений websocket
        :param atasks: Ссылка на список асинхронных задач
        :param update_rate: период обновления датчика, [s]
        """
        super().__init__(
            title=title,
            resource_id=resource_id,
            ws=ws,
            update_rate=update_rate,
        )
        self.__data_presence = SigBool()
        # данные
        self._data.extend(
            [
                self.__data_presence,
            ],
        )
        atasks.append(self.task())

    async def presence(self: "Presence", update: bool = False) -> SigBool:
        """Состояние - есть движеиние.

        :param update: True - опрос, False - из памяти
        :return: состояние датчика
        """
        if update:
            await self._update()
        return await asleep(0, self.__data_presence)

    async def _task(self: "Presence") -> None:
        await super()._task()
        # проверка сообщений websocket
        msg = self._ws.get_msg_presence(self._id)
        if msg is not None:
            log.debug(
                "%s: в очереди новое сообщение: %s",
                repr(self),
                msg.state.presence,
            )
            self.__data_presence.update(msg.state.presence, Qual.GOOD)
        return await asleep(0)

    async def _update(self: "Presence") -> None:
        """Принудительно обновить данные.

        :return: none
        """
        msg = await self._api_get_sensor()
        if msg is None:
            return await asleep(0)
        data = schemas.ZHAPresence.parse_obj(msg.json())
        self.__data_presence.update(data.state.presence, Qual.GOOD)
        return await asleep(0)


class LightLevel(BaseSensor):
    """ZHALightLevel."""

    def __init__(
        self: "LightLevel",
        title: str,
        resource_id: int,
        ws: deconz.Websocket,
        atasks: list[Coroutine[Any, Any, None]],
        update_rate: float = 5.0,
    ) -> None:
        """Датчик уровня освещенности.

        :param title: название датчика
        :param resource_id: id сенсора
        :param ws: Канал сообщений websocket
        :param atasks: Ссылка на список асинхронных задач
        :param update_rate: период обновления датчика, [s]
        """
        super().__init__(
            title=title,
            resource_id=resource_id,
            ws=ws,
            update_rate=update_rate,
        )
        self.__data_lux = SigFloat(unit=Units.DEG_CELSIUS)
        # данные
        self._data.extend(
            [
                self.__data_lux,
            ],
        )
        atasks.append(self.task())

    async def lux(self: "LightLevel", update: bool = False) -> SigFloat:
        """Состояние - открыт или закрыт.

        :param update: True - опрос, False - из памяти
        :return: состояние датчика
        """
        if update:
            await self._update()
        return await asleep(0, self.__data_lux)

    async def _task(self: "LightLevel") -> None:
        await super()._task()
        # проверка сообщений websocket
        msg = self._ws.get_msg_light_level(self._id)
        if msg is not None:
            log.debug(
                "%s: в очереди новое сообщение: %s",
                repr(self),
                msg,
            )
            # websocket не возвращает state !!! - возможно баг
            # self.__data_lux.update(msg.state, Qual.GOOD)
        return await asleep(0)

    async def _update(self: "LightLevel") -> None:
        """Принудительно обновить данные.

        :return: none
        """
        msg = await self._api_get_sensor()
        if msg is None:
            return await asleep(0)
        data = schemas.ZHALightLevel.parse_obj(msg.json())
        self.__data_lux.update(data.state.lux, Qual.GOOD)
        return await asleep(0)


class Humidity(BaseSensor):
    """ZHAHumidity."""

    class Schema(BaseSensor.Schema):
        """Схема для API."""

        humidity: SigFloat.Schema

    def __init__(
        self: "Humidity",
        title: str,
        resource_id: int,
        ws: deconz.Websocket,
        atasks: list[Coroutine[Any, Any, None]],
        update_rate: float = 5.0,
    ) -> None:
        """Датчик влажности.

        :param title: название датчика
        :param resource_id: id сенсора
        :param ws: Канал сообщений websocket
        :param update_rate: период обновления датчика, [s]
        :param atasks: ссылка на список с задачами asyncio
        """
        super().__init__(
            title=title,
            resource_id=resource_id,
            ws=ws,
            update_rate=update_rate,
        )
        self.__data_hum = SigFloat(unit=Units.PERCENT)
        # данные
        self._data.extend(
            [
                self.__data_hum,
            ],
        )
        atasks.append(self.task())

    @property
    def schema(self: "Humidity") -> Schema:
        """Схема для API.

        :return: схема для API
        """
        return self.Schema(
            title=self._title,
            humidity=self.__data_hum.schema,
        )

    async def humidity(self: "Humidity", update: bool = False) -> SigFloat:
        """Состояние - открыт или закрыт.

        :param update: True - опрос, False - из памяти
        :return: состояние датчика
        """
        if update:
            await self._update()
        return await asleep(0, self.__data_hum)

    async def _task(self: "Humidity") -> None:
        await super()._task()
        # проверка сообщений websocket
        msg = self._ws.get_msg_humidity(self._id)
        if msg is not None:
            log.debug(
                "%s: в очереди новое сообщение: %s",
                repr(self),
                msg,
            )
            self.__data_hum.update(msg.state.humidity / 100, Qual.GOOD)
        return await asleep(0)

    async def _update(self: "Humidity") -> None:
        """Принудительно обновить данные.

        :return: none
        """
        msg = await self._api_get_sensor()
        if msg is None:
            return await asleep(0)
        data = schemas.ZHAHumidity.parse_obj(msg.json())
        self.__data_hum.update(data.state.humidity / 100, Qual.GOOD)
        return await asleep(0)


class ZHATemperature(BaseSensor):
    """ZHATemperature."""

    class Schema(BaseSensor.Schema):
        """Схема для API."""

        temperature: SigFloat.Schema

    def __init__(
        self: Self,
        title: str,
        resource_id: int,
        ws: deconz.Websocket,
        atasks: list[Coroutine[Any, Any, None]],
        update_rate: float = 10.0,
    ) -> None:
        """Датчик температуры.

        :param title: название датчика
        :param resource_id: id сенсора
        :param ws: Канал сообщений websocket
        :param update_rate: период обновления датчика, [s]
        :param atasks: ссылка на список с задачами asyncio
        """
        super().__init__(
            title=title,
            resource_id=resource_id,
            ws=ws,
            update_rate=update_rate,
        )
        self.__data_temp = SigFloat(unit=Units.DEG_CELSIUS)
        # данные
        self._data.extend(
            [
                self.__data_temp,
            ],
        )
        atasks.append(self.task())

    @property
    def schema(self: Self) -> Schema:
        """Схема для API.

        :return: схема для API
        """
        return self.Schema(
            title=self._title,
            temperature=self.__data_temp.schema,
        )

    async def temperature(self: Self, update: bool = False) -> SigFloat:
        """Значение температуры.

        :param update: True - опрос, False - из памяти
        :return: состояние датчика
        """
        if update:
            await self._update()
        return await asleep(0, self.__data_temp)

    async def _task(self: Self) -> None:
        await super()._task()
        # проверка сообщений websocket
        msg = self._ws.get_msg_temperature(self._id)
        if msg is not None:
            log.debug(
                "%s: в очереди новое сообщение: %s",
                repr(self),
                msg,
            )
            self.__data_temp.update(msg.state.temperature / 100, Qual.GOOD)
        return await asleep(0)

    async def _update(self: Self) -> None:
        """Принудительно обновить данные.

        :return: none
        """
        msg = await self._api_get_sensor()
        if msg is None:
            return await asleep(0)
        data = schemas.ZHATemperature.parse_obj(msg.json())
        self.__data_temp.update(data.state.temperature / 100, Qual.GOOD)
        return await asleep(0)


class ZHAPressure(BaseSensor):
    """ZHAPressure."""

    class Schema(BaseSensor.Schema):
        """Схема для API."""

        pressure: SigFloat.Schema

    def __init__(
        self: Self,
        title: str,
        resource_id: int,
        ws: deconz.Websocket,
        atasks: list[Coroutine[Any, Any, None]],
        update_rate: float = 10.0,
    ) -> None:
        """Датчик температуры.

        :param title: название датчика
        :param resource_id: id сенсора
        :param ws: Канал сообщений websocket
        :param update_rate: период обновления датчика, [s]
        :param atasks: ссылка на список с задачами asyncio
        """
        super().__init__(
            title=title,
            resource_id=resource_id,
            ws=ws,
            update_rate=update_rate,
        )
        self.__data_pressure = SigFloat(unit=Units.DEG_CELSIUS)
        # данные
        self._data.extend(
            [
                self.__data_pressure,
            ],
        )
        atasks.append(self.task())

    @property
    def schema(self: Self) -> Schema:
        """Схема для API.

        :return: схема для API
        """
        return self.Schema(
            title=self._title,
            pressure=self.__data_pressure.schema,
        )

    async def pressure(self: Self, update: bool = False) -> SigFloat:
        """Значение давления.

        :param update: True - опрос, False - из памяти
        :return: состояние датчика
        """
        if update:
            await self._update()
        return await asleep(0, self.__data_pressure)

    async def _task(self: Self) -> None:
        await super()._task()
        # проверка сообщений websocket
        msg: schemas.ZHAPressureWs | None = self._ws.get_msg_pressure(self._id)
        if msg is not None:
            log.debug(
                "%s: в очереди новое сообщение: %s",
                repr(self),
                msg,
            )
            self.__data_pressure.update(msg.state.pressure, Qual.GOOD)
        return await asleep(0)

    async def _update(self: Self) -> None:
        """Принудительно обновить данные.

        :return: none
        """
        msg = await self._api_get_sensor()
        if msg is None:
            return await asleep(0)
        data = schemas.ZHAPressure.parse_obj(msg.json())
        self.__data_pressure.update(data.state.pressure, Qual.GOOD)
        return await asleep(0)
