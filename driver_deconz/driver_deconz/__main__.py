"""Запуск сервиса."""
import asyncio
import logging

from shared.async_tasks import TasksRunner
from shared.logger import Logger
from shared.settings import SettingsStore

from .api.api_task import ApiTask
from .deconz import sensors
from .deconz.main import Deconz

Logger(output_to_console=True)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


settings = SettingsStore("../.env").settings

sensors = sensors.SensorCollection(
    sensors={
        sensors.OpenClose(
            uniqueid="00:15:8d:00:03:21:44:8c-01-0006",
            name="open_close",
        ),
        # BaseSensor[sensor_types.ZHAHumidity](
        #     uniqueid=6,
        #     name="humidity",
        #     model=sensor_types.ZHAHumidity,
        # ),
        # BaseSensor[sensor_types.ZHATemperature](
        #     uniqueid=7,
        #     name="temperature",
        #     model=sensor_types.ZHATemperature,
        # ),
        # BaseSensor[sensor_types.ZHAPressure](
        #     uniqueid=8,
        #     name="pressure",
        #     model=sensor_types.ZHAPressure,
        # ),
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
