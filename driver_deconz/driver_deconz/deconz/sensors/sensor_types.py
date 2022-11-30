"""Схемы типов датчиков."""
import datetime as dt

from pydantic import BaseModel


class ZHAHumidity(BaseModel):
    """Датчик влажности."""

    humidity: int = 0
    lastupdated: dt.datetime = dt.datetime.min


class ZHAPressure(BaseModel):
    """Датчик давления."""

    pressure: int = 0
    lastupdated: dt.datetime = dt.datetime.min


class ZHATemperature(BaseModel):
    """Датчик температуры."""

    temperature: int = 0
    lastupdated: dt.datetime = dt.datetime.min
