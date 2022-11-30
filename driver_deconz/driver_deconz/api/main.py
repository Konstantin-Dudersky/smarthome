"""API."""

from typing import Any

from fastapi import Depends, FastAPI, Path

from ..deconz.sensors.base_sensor import BaseSensor
from . import depends

app = FastAPI()


@app.get("/sensor-by-id/{ident}")
def sensor_by_ident(
    ident: int = Path(),
    sensors: depends.sensors_type = Depends(depends.sensors_depends),
) -> BaseSensor[Any]:
    """Данные дачтика по идентификатору."""
    return sensors.by_id(ident).sensor_data


@app.get("/sensor-by-name/{name}")
def sensor_by_name(
    name: str = Path(),
    sensors: depends.sensors_type = Depends(depends.sensors_depends),
) -> BaseSensor[Any]:
    """Данные датчика по имени."""
    return sensors.by_name(name).sensor_data
