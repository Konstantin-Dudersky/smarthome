"""API."""

# pyright: reportUnusedFunction=false

from typing import Any

from shared.fastapi import BaseApi, Depends, FastAPI, Path

from ..deconz.sensors import SensorCollection
from ..deconz.sensors.base_sensor import BaseSensor
from .dependencies import Dependencies


def _configure_endpoints(app: FastAPI, depends: Dependencies):
    @app.get("/sensors")
    def all_sensors(
        sensors: depends.sensors_type = Depends(depends.sensors),
    ) -> dict[str, BaseSensor[Any]]:
        """Данные всех датчиков."""
        return {
            uniqueid: sensor.sensor_data
            for uniqueid, sensor in sensors.all_by_name.items()
        }

    @app.get("/sensor-by-name/{name}")
    def sensor_by_name(
        name: str = Path(),
        sensors: depends.sensors_type = Depends(depends.sensors),
    ) -> BaseSensor[Any]:
        """Данные датчика по имени."""
        return sensors.by_name(name).sensor_data


class Api(BaseApi):
    """API."""

    def __init__(
        self,
        depends_sensors: SensorCollection,
        port: int = 8000,
    ) -> None:
        """Construct API."""
        super().__init__(port=port)
        self.__depends = Dependencies(
            sensors=depends_sensors,
        )
        _configure_endpoints(self.app, self.__depends)
