"""Запуск сервиса."""
import asyncio
import logging

from shared.async_tasks import TasksRunner
from shared.logger import Logger
from shared.settings import SettingsStore

from .api.api_task import ApiTask
from .deconz import sensor_types
from .deconz.main import Deconz
from .deconz.sensor import Sensor
from .deconz.sensors_collection import SensorCollection

Logger(output_to_console=True)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


settings = SettingsStore("../.env").settings

sensors = SensorCollection(
    sensors={
        Sensor[sensor_types.ZHAOpenClose](
            identificator=2,
            name="open_close",
            model=sensor_types.ZHAOpenClose,
        ),
        Sensor[sensor_types.ZHAHumidity](
            identificator=6,
            name="humidity",
            model=sensor_types.ZHAHumidity,
        ),
        Sensor[sensor_types.ZHATemperature](
            identificator=7,
            name="temperature",
            model=sensor_types.ZHATemperature,
        ),
        Sensor[sensor_types.ZHAPressure](
            identificator=8,
            name="pressure",
            model=sensor_types.ZHAPressure,
        ),
    },
)

runner = TasksRunner(
    {
        Deconz(
            host=settings.deconz_hub_host,
            port_api=settings.deconz_hub_port_api,
            port_ws=settings.deconz_hub_port_ws,
            api_key=settings.deconz_hub_api_key,
            sensosrs=sensors,
        ),
        ApiTask(settings.driver_deconz_port),
    },
)


def main() -> None:
    """Entry point."""
    asyncio.run(runner())


if __name__ == "__main__":
    main()
