"""Sensors/switches in deconz."""

import asyncio
from datetime import datetime
from enum import Enum, auto

from .api import get_sensor

class SensorStates(Enum):
    INIT = auto()
    

class OpenClose:
    """ZHAOpenClose."""

    def __init__(self: "OpenClose") -> None:
        self.__lastupdated: datetime | None = None
        self.__lowbattery: bool = False
        self.__open: bool = False
        self.__tampered: bool = False

    async def run(self: "OpenClose") -> None:
        while True:
            await self.__run()

    async def __run(self: "OpenClose") -> None:
        print("sensor work!")
        await asyncio.sleep(1)
