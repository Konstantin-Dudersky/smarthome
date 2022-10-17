"""Взаимодействие с лампами yeelight.

Описание API - https://www.yeelight.com/en_US/developer

Пример реализации - https://gitlab.com/stavros/python-yeelight
"""

import asyncio
from asyncio import sleep as asleep
from enum import Enum
from typing import Any, Coroutine, NamedTuple

from pydantic import BaseModel, Field, ValidationError

from src.base.logic import CyclicRun
from src.base.signals import (
    Qual,
    Scale,
    SigBool,
    SigFloat,
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


class _SigBright(SigFloat):
    """Яркость."""

    def __init__(
        self: "_SigBright",
        comm_class: "Bulb",
    ) -> None:
        """Яркость.

        :param comm_class: ссылка на класс коммуникации
        """
        super().__init__(unit=Units.LUX)
        self.__comm_class = comm_class

    def read(self: "_SigBright") -> None:
        """Запланировать чтение данных."""

        async def _read() -> None:
            msg = await self.__comm_class.get_prop("bright")
            if msg is None:
                self.qual = Qual.BAD
            else:
                self.value = float(msg.result[0])
                self.qual = Qual.GOOD

        self._coro_read = _read()

    def write(
        self: "_SigBright",
        brightness: int,
        effect: Effects = Effects.SMOOTH,
        duration: int = 200,
    ) -> None:
        """Запланировать запись данных.

        :param brightness: Значение яркости в процентах (1-100%)
        :param effect: Эффект перехода
        :param duration: Время перехода, [мс]
        """

        async def _write() -> None:
            msg = CommandMessage(
                id=1,
                method="set_bright",
                params=[brightness, effect.value, duration],
            )
            await self.__comm_class.send_command(str(msg))
            self.read()

        self._coro_write = _write()


class _SigCt(SigFloat):
    """Цветовая температура."""

    def __init__(
        self: "_SigCt",
        comm_class: "Bulb",
    ) -> None:
        """Цветовая температура.

        :param comm_class: ссылка на класс коммуникации
        """
        super().__init__(unit=Units.KELVIN, scale=Scale(1700, 6500))
        self.__comm_class = comm_class

    def read(self: "_SigCt") -> None:
        """Запланировать чтение данных."""

        async def _read() -> None:
            msg = await self.__comm_class.get_prop("ct")
            if msg is None:
                self.qual = Qual.BAD
            else:
                self.value = float(msg.result[0])
                self.qual = Qual.GOOD

        self._coro_read = _read()

    def write(
        self: "_SigCt",
        ct_value: int,
        effect: Effects = Effects.SMOOTH,
        duration: int = 200,
    ) -> None:
        """Запланировать запись данных.

        :param ct_value: Цветовая температура (1700-6500K)
        :param effect: Эффект перехода
        :param duration: Время перехода, [мс]
        """

        async def _write() -> None:
            msg = CommandMessage(
                id=1,
                method="set_ct_abx",
                params=[ct_value, effect.value, duration],
            )
            await self.__comm_class.send_command(str(msg))
            self.read()

        self._coro_write = _write()


class _SigColorMode(SigFloat):
    """Режим цвета лампы."""

    def __init__(
        self: "_SigColorMode",
        comm_class: "Bulb",
    ) -> None:
        """Режим цвета лампы.

        :param comm_class: ссылка на класс коммуникации
        """
        super().__init__(unit=Units.LUX)
        self.__comm_class = comm_class

    def read(self: "_SigColorMode") -> None:
        """Запланировать чтение данных."""

        async def _read() -> None:
            msg = await self.__comm_class.get_prop("color_mode")
            if msg is None:
                self.qual = Qual.BAD
            else:
                self.value = float(msg.result[0])
                self.qual = Qual.GOOD

        self._coro_read = _read()


class _SigPower(SigBool):
    """Включена ли лампа."""

    def __init__(
        self: "_SigPower",
        comm_class: "Bulb",
    ) -> None:
        """Цветовая температура.

        :param comm_class: ссылка на класс коммуникации
        """
        super().__init__()
        self.__comm_class = comm_class

    def read(self: "_SigPower") -> None:
        """Запланировать чтение данных."""

        async def _read() -> None:
            msg = await self.__comm_class.get_prop("power")
            if msg is None:
                self.qual = Qual.BAD
            else:
                self.value = onoff_to_bool(msg.result[0])
                self.qual = Qual.GOOD

        self._coro_read = _read()

    def write(
        self: "_SigPower",
        power: bool,
        effect: Effects = Effects.SMOOTH,
        duration: int = 200,
    ) -> None:
        """Запланировать запись данных.

        :param power: Включить или выключить
        :param effect: Эффект перехода
        :param duration: Время перехода, [мс]
        """

        async def _write() -> None:
            msg = CommandMessage(
                id=1,
                method="set_power",
                params=[bool_to_onoff(power), effect.value, duration],
            )
            await self.__comm_class.send_command(str(msg))
            self.read()

        self._coro_write = _write()


class _SigRgb(SigFloat):
    """Цвет."""

    def __init__(
        self: "_SigRgb",
        comm_class: "Bulb",
    ) -> None:
        """Яркость.

        :param comm_class: ссылка на класс коммуникации
        """
        super().__init__(unit=Units.LUX)
        self.__comm_class = comm_class

    def read(self: "_SigRgb") -> None:
        """Запланировать чтение данных."""

        async def _read() -> None:
            msg = await self.__comm_class.get_prop("rgb")
            if msg is None:
                self.qual = Qual.BAD
            else:
                self.value = float(msg.result[0])
                self.qual = Qual.GOOD

        self._coro_read = _read()

    def write(
        self: "_SigRgb",
        rgb_value: int,
        effect: Effects = Effects.SMOOTH,
        duration: int = 200,
    ) -> None:
        """Запланировать запись данных.

        :param rgb_value: Значение цвета (0..16777215)
        :param effect: Эффект перехода
        :param duration: Время перехода, [мс]
        """

        async def _write() -> None:
            msg = CommandMessage(
                id=1,
                method="set_rgb",
                params=[rgb_value, effect.value, duration],
            )
            await self.__comm_class.send_command(str(msg))
            self.read()

        self._coro_write = _write()


class BulbSchema(BaseModel):
    """Данные лампы."""

    power: _SigPower.Schema
    bright: _SigBright.Schema
    color_mode: _SigColorMode.Schema
    ct: _SigCt.Schema
    rgb: _SigRgb.Schema


class Bulb:
    """Лампа."""

    class _Data2(NamedTuple):
        bright: _SigBright
        ct: _SigCt
        power: _SigPower
        color_mode: _SigColorMode
        rgb: _SigRgb

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
        self.__reachable = True
        self.__cyclic_update = CyclicRun(10.0)  # циклическое обновление
        atasks.append(self.__task())
        self.__data2 = self._Data2(
            bright=_SigBright(comm_class=self),
            ct=_SigCt(comm_class=self),
            power=_SigPower(comm_class=self),
            color_mode=_SigColorMode(comm_class=self),
            rgb=_SigRgb(comm_class=self),
        )

    @property
    def data(self: "Bulb") -> _Data2:
        """Данные лампы.

        :return: данные лампы
        """
        return self.__data2

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
                power=self.__data2.power.schema,
                bright=self.__data2.bright.schema,
                color_mode=self.__data2.color_mode.schema,
                ct=self.__data2.ct.schema,
                rgb=self.__data2.rgb.schema,
            ),
        )

    async def __task(self: "Bulb") -> None:
        """Задача для циклического выполнения."""
        while True:
            await self.__update()
            await asleep(0)

    async def __update(self: "Bulb") -> None:
        if self.__cyclic_update():
            for sig in self.__data2:
                sig.read()
        for sig in self.__data2:
            await sig.read_exec()
        for sig in self.__data2:
            await sig.write_exec()
        await asleep(0)

    async def get_prop(
        self: "Bulb",
        prop: str,
    ) -> ResultMessageGood | None:
        """Retrieve current property of smart LED.

        :param prop: Запрашиваемое свойство
        :return: Ответное сообщение или None
        """
        msg = CommandMessage(
            id=1,
            method="get_prop",
            params=[prop],
        )
        return await self.send_command(str(msg))

    async def send_command(
        self: "Bulb",
        msg: str,
    ) -> ResultMessageGood | None:
        """Послать команду в лампу.

        :raises ValueError: невозможно распознать ответ
        :param msg: сообщение для передачи
        :return: ответное сообщение или None при неудаче
        """
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
        bulb.data.power.write(True)
        while True:
            value += 5
            if value > 100:
                value = 1
            bulb.data.bright.write(value)
            await asyncio.sleep(0.5)

    asyncio.run(run())
