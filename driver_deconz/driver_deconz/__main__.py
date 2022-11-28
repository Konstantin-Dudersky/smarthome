"""Запуск сервиса."""
import asyncio
import logging

from shared import Logger

from .deconz import sensor_types
from .deconz.main import Deconz
from .deconz.sensor import Sensor
from .deconz.sensors_collection import SensorCollection

Logger(output_to_console=True)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# settings = settings_store.settings

from shared import SettingsStore

settings = SettingsStore("../.env").settings

import sys

sys.exit(0)

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

dz = Deconz(
    host=settings.deconz_hub_host,
    port_ws=settings.deconz_hub_port_ws,
    sensosrs=sensors,
)


async def run() -> None:
    """Create main task."""
    done, _ = await asyncio.wait(
        [
            *[asyncio.create_task(task) for task in dz.async_tasks],
        ],
        return_when=asyncio.FIRST_COMPLETED,
    )
    try:
        _ = [d.result() for d in done]
    except BaseException:  # noqa: WPS424
        log.exception(
            "Необработанное исключение, программа заканчивает выполнение",
        )


if __name__ == "__main__":
    asyncio.run(run())
