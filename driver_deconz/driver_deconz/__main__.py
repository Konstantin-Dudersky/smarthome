"""Запуск сервиса."""
import asyncio
import logging

from shared.async_tasks import TasksRunner
from shared.logger import Logger
from shared.messagebus import MessageBus
from shared.redis_publisher import RedisPublisher
from shared.settings import SettingsStore

from .api.main import Api
from .deconz import sensors
from .deconz.main import Deconz

Logger(output_to_console=True)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


settings = SettingsStore("../.env").settings

messagebus = MessageBus()

sensors = sensors.SensorCollection(
    sensors={
        sensors.OpenClose(
            uniqueid="00:15:8d:00:03:21:44:8c-01-0006",
            name="open_close",
        ),
        sensors.Temperature(
            uniqueid="00:15:8d:00:03:f0:44:0d-01-0402",
            name="temperature",
        ),
        sensors.Pressure(
            uniqueid="00:15:8d:00:03:f0:44:0d-01-0403",
            name="pressure",
        ),
        sensors.Humidity(
            uniqueid="00:15:8d:00:03:f0:44:0d-01-0405",
            name="humidity",
        ),
        sensors.Daylight(
            uniqueid="00:21:2e:ff:ff:04:82:3b-01",
            name="daylight",
        ),
    },
    messagebus=messagebus,
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
        Api(
            port=settings.driver_deconz_port,
            depends_sensors=sensors,
        ),
        RedisPublisher(
            host=settings.redis_host,
            port=settings.redis_port,
            messagebus=messagebus,
        ),
    },
)


def main() -> None:
    """Entry point."""
    asyncio.run(runner())


if __name__ == "__main__":
    main()
