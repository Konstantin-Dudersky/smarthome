"""Взаимодействие с лампами yeelight.

Описание API - https://www.yeelight.com/en_US/developer

Пример реализации - https://gitlab.com/stavros/python-yeelight
"""

import asyncio
from asyncio import sleep as asleep
from enum import Enum
from typing import Any, Coroutine

from pydantic import BaseModel, Field, ValidationError

from src.base.logic import CyclicRun
from src.base.types import (
    Qual,
    SigBool,
    SigBoolSchema,
    SigFloat,
    SigFloatSchema,
    Units,
)

if __name__ == "__main__":
    import logging

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
else:
    from src.utils.logger import LoggerLevel, get_logger

    logger = get_logger(__name__, LoggerLevel.INFO)


def bool_to_onoff(value: bool) -> str:
    """Преобразует значение типа bool в on/off.

    :param value: Преобразуемое значение
    :return: on/off
    """
    return "on" if value else "off"


def onoff_to_bool(value: str) -> bool:
    """Преобразует значение типа on/off в тип bool.

    :raises ValueError: Неправильное значение
    :param value: Преобразуемое значение
    :return: bool
    """
    match value:
        case "on":
            return True
        case "off":
            return False
        case _:
            raise ValueError(f"Невозможно преобразовать в bool: {value}")
    return False


class Properties(Enum):
    """Доступные свойства."""

    POWER = "power"
    BRIGHT = "bright"


class Effects(Enum):
    """Эффекты перехода."""

    SUDDEN = "sudden"
    SMOOTH = "smooth"


class CommandMessage(BaseModel):
    """Команда."""

    msg_id: int = Field(..., alias="id")
    method: str
    params: list[int | str]

    def __str__(self: "CommandMessage") -> str:
        """Строковое представление.

        :return: строка формата JSON
        """
        return self.json(by_alias=True) + "\r\n"


class ResultMessageGood(BaseModel):
    """Успешный ответ."""

    msg_id: int = Field(..., alias="id")
    result: list[str]


class ResultMessageError(BaseModel):
    """Неуспешный ответ."""

    msg_id: int = Field(..., alias="id")
    error: dict[str, Any]


class BulbSchema(BaseModel):
    """Данные лампы."""

    power: SigBoolSchema
    bright: SigFloatSchema


class Bulb:
    """Лампа."""

    def __init__(
        self: "Bulb",
        ip_address: str,
        atasks: list[Coroutine[Any, Any, None]],
        port: int = 55443,
    ) -> None:
        """Лампа.

        :param ip_address: ip-адрес лампы
        :param port: tcp-порт
        :param atasks: ссылка на список асинхронных задач
        """
        self.__ip = ip_address
        self.__port = port
        # properties
        self.__data_power = SigBool()
        self.__data_bright = SigFloat(unit=Units.PERCENT)
        self.__reachable = True
        self.__cyclic_update = CyclicRun(10.0)  # циклическое обновление
        atasks.append(self.__task())

    async def get_all_data(self: "Bulb", update: bool = False) -> BulbSchema:
        """Получить все данные.

        :param update: True - опрос лампы, False - из памяти
        :return: данные
        """
        if update:
            await self.__update()
        return await asleep(
            0,
            BulbSchema(
                power=self.__data_power.schema,
                bright=self.__data_bright.schema,
            ),
        )

    async def get_bright(self: "Bulb", update: bool = False) -> SigFloat:
        """Яркость в процентах.

        :param update: True - опрос лампы, False - из памяти
        :return: Яркость в процентах (1 - 100%)
        """
        if update:
            msg = await self.__get_prop(Properties.BRIGHT)
            if msg is None:
                self.__data_bright.qual = Qual.BAD
                return self.__data_bright
            self.__data_bright.update(float(msg.result[0]), Qual.GOOD)
        return self.__data_bright

    async def set_bright(
        self: "Bulb",
        brightness: int,
        effect: Effects = Effects.SMOOTH,
        duration: int = 200,
    ) -> None:
        """Изменить яркость.

        :param brightness: Значение яркости в процентах (1-100%)
        :param effect: Эффект перехода
        :param duration: Время перехода, [мс]
        """
        msg = CommandMessage(
            id=1,
            method="set_bright",
            params=[brightness, effect.value, duration],
        )
        await self.__send_command(str(msg))
        await self.get_bright(True)

    async def get_power(self: "Bulb", update: bool = False) -> SigBool:
        """Включена ли лампа.

        :param update: True - опрос лампы, False - из памяти
        :return: Включена ли лампа
        """
        if update:
            msg = await self.__get_prop(Properties.POWER)
            if msg is None:
                self.__data_power.qual = Qual.BAD
                return self.__data_power
            self.__data_power.update(onoff_to_bool(msg.result[0]), Qual.GOOD)
        return self.__data_power

    async def set_power(
        self: "Bulb",
        power: bool,
        effect: Effects = Effects.SMOOTH,
        duration: int = 200,
    ) -> None:
        """Включить или выключить лампу.

        :param power: Включить или выключить
        :param effect: Эффект перехода
        :param duration: Время перехода, [мс]
        """
        msg = CommandMessage(
            id=1,
            method="set_power",
            params=[bool_to_onoff(power), effect.value, duration],
        )
        await self.__send_command(str(msg))
        await self.get_power(True)

    async def __task(self: "Bulb") -> None:
        """Задача для циклического выполнения."""
        while True:
            if self.__cyclic_update():
                await self.__update()
            await asyncio.sleep(0)

    async def __update(self: "Bulb") -> None:
        await self.get_power(True)
        await self.get_bright(True)

    async def __get_prop(
        self: "Bulb",
        prop: Properties,
    ) -> ResultMessageGood | None:
        """Retrieve current property of smart LED.

        :param prop: Запрашиваемое свойство
        :return: Ответное сообщение или None
        """
        msg = CommandMessage(
            id=1,
            method="get_prop",
            params=[prop.value],
        )
        return await self.__send_command(str(msg))

    async def __send_command(
        self: "Bulb",
        msg: str,
    ) -> ResultMessageGood | None:
        if not self.__cyclic_update.started:
            logger.warning(
                "%s, не запущено циклическое обновление",
                repr(self),
            )
        logger.debug("Send command buld: %r", self)
        fut = asyncio.open_connection(self.__ip, self.__port)
        try:
            reader, writer = await asyncio.wait_for(fut, timeout=3)
            self.__reachable = True
        except asyncio.TimeoutError:
            if self.__reachable:
                logger.exception("%s: timeout", repr(self))
                self.__reachable = False
            return await asleep(0)
        except OSError:
            if self.__reachable:
                self.__reachable = False
                logger.exception("%s: невозможно подлючиться", repr(self))
            return await asleep(0)
        logger.debug("Send: %r", msg)
        writer.write(msg.encode())
        await writer.drain()
        result = (await reader.readuntil(b"\r\n")).decode()
        logger.debug("Received: %r", result)
        writer.close()
        await writer.wait_closed()
        try:
            return ResultMessageGood.parse_raw(result)
        except ValidationError:
            pass
        try:
            error = ResultMessageError.parse_raw(result)
            logger.error(
                "Команда не выполнена,\nзапрос: %r\nответ: %r",
                msg,
                error.error,
            )
            return None
        except ValidationError as exc:
            raise ValueError(f"Незвестный формат ответа:\n {result}") from exc

    def __repr__(self: "Bulb") -> str:
        """Represent string.

        :return: string representaion
        """
        return f"Yeelight bulb: {self.__ip}"


if __name__ == "__main__":
    tasks = []
    bulb = Bulb("192.168.101.20", atasks=tasks)

    async def run() -> None:
        """Task."""
        value = 1
        await bulb.set_power(True)
        while True:
            value += 5
            if value > 100:
                value = 1
            await bulb.set_bright(value)
            await asyncio.sleep(0.5)

    asyncio.run(run())
