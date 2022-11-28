"""Схемы типов датчиков."""
import datetime as dt
from typing import Annotated

from pydantic import BaseModel, Field


class ZHAHumidity(BaseModel):
    """Датчик влажности."""

    humidity: int = 0
    lastupdated: dt.datetime = dt.datetime.min


class ZHAOpenCloseState(BaseModel):
    """Датчик открытия / закрытия - состояние."""

    open: bool = False
    lastupdated: dt.datetime = dt.datetime.min
    lowbattery: bool | None
    tampered: bool | None


class ZHAOpenClose(BaseModel):
    """Датчик открытия / закрытия."""

    state: ZHAOpenCloseState = ZHAOpenCloseState.construct()
    lastseen: dt.datetime = dt.datetime.min
    uniqueid: str | None


class ZHAPressure(BaseModel):
    """Датчик давления."""

    pressure: int = 0
    lastupdated: dt.datetime = dt.datetime.min


class ZHATemperature(BaseModel):
    """Датчик температуры."""

    temperature: int = 0
    lastupdated: dt.datetime = dt.datetime.min
