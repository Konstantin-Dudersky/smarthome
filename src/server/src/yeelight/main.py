"""Взаимодействие с лампами yeelight.

Описание API - https://www.yeelight.com/en_US/developer

Пример реализации - https://gitlab.com/stavros/python-yeelight
"""

import asyncio
from enum import Enum
import time
from typing import Any

from pydantic import BaseModel, Field, ValidationError

if __name__ == "__main__":
    import logging

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
else:
    from src.utils.logger import LoggerLevel, get_logger

    logger = get_logger(__name__)
    logger.setLevel(LoggerLevel.DEBUG)


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


class Bulb:
    """Лампа."""

    def __init__(
        self: "Bulb",
        ip_address: str,
        port: int = 55443,
    ) -> None:
        """Лампа.

        :param ip_address: ip-адрес лампы
        :param port: tcp-порт
        """
        self.__ip = ip_address
        self.__port = port
        # properties
        self.__power: bool | None = None
        self.__bright: int | None = None

        self.__cyclic_update = CyclicRun(10.0)  # циклическое обновление

    async def get_power(self: "Bulb", update: bool = False) -> bool | None:
        """Включена ли лампа.

        :param update: True - опрос лампы, False - из памяти
        :return: Включена ли лампа
        """
        if update:
            msg = await self._get_prop(Properties.POWER)
            if msg is None:
                return self.__power
            self.__power = onoff_to_bool(msg.result[0])
        return self.__power

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
        await self._send_command(str(msg))
        await self.get_power(True)

    async def get_bright(self: "Bulb", update: bool = False) -> int | None:
        """Яркость в процентах.

        :param update: True - опрос лампы, False - из памяти
        :return: Яркость в процентах (1 - 100%)
        """
        if update:
            msg = await self._get_prop(Properties.BRIGHT)
            if msg is None:
                return self.__bright
            self.__bright = int(msg.result[0])
        return self.__bright

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
        await self._send_command(str(msg))
        await self.get_bright(True)

    async def run(self: "Bulb") -> None:
        """Задача для циклического выполнения."""
        if self.__cyclic_update.run:
            await self.get_power(True)
            await self.get_bright(True)
        await asyncio.sleep(0)

    async def _get_prop(
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
        return await self._send_command(str(msg))

    async def _send_command(
        self: "Bulb",
        msg: str,
    ) -> ResultMessageGood | None:
        if not self.__cyclic_update.started:
            logger.warning(
                "%s, не запущено циклическое обновление",
                repr(self),
            )
        logger.debug("Send command buld: %r", self)
        try:
            reader, writer = await asyncio.open_connection(
                self.__ip,
                self.__port,
            )
        except OSError:
            logger.exception("%s, невозможно подлючиться", repr(self))
            return None
        logger.debug("Send: %r", msg)
        writer.write(msg.encode())
        await writer.drain()
        result = (await reader.read(100)).decode()
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
        return f"Bulb: {self.__ip}"


if __name__ == "__main__":
    bulb = Bulb("192.168.101.20")

    async def run() -> None:
        """Task."""
        value = 1
        await bulb.set_power(True)
        while True:
            value += 5
            if value > 100:
                value = 1
            await bulb.run()
            await bulb.set_bright(value)
            await asyncio.sleep(0.5)

    asyncio.run(run())
