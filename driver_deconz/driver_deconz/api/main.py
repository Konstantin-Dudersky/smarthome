"""API."""

from typing import Any

from fastapi import Depends, FastAPI, Path

from ..deconz.sensor import Sensor
from . import depends

app = FastAPI()


@app.get("/sensor-by-id/{ident}")
def sensor_by_ident(
    ident: int = Path(),
    sensors: depends.sensors_type = Depends(depends.sensors_depends),
) -> Sensor[Any]:
    """Данные дачтика по идентификатору."""
    return sensors.by_id(ident).data


@app.get("/sensor-by-name/{name}")
def sensor_by_name(
    name: str = Path(),
    sensors: depends.sensors_type = Depends(depends.sensors_depends),
) -> Sensor[Any]:
    """Данные датчика по имени."""
    return sensors.by_name(name).data
