"""Main script for server."""

import asyncio

from src.utils.settings import settings
from src.utils.telegram import bot
from src.utils.logger import LoggerLevel, get_logger

from .base import logic
from .deconz import Websocket
from .deconz import sensors
from .yeelight import Bulb

logger = get_logger(__name__, LoggerLevel.INFO)

deconz_ws = Websocket()
sensor1 = sensors.OpenClose(2, deconz_ws)
sensor_presence = sensors.Presence(3, deconz_ws)
bulb = Bulb("192.168.101.20")


async def _run() -> None:
    pos_front = logic.PosFront()
    neg_front = logic.NegFront()
    while True:
        presence = await sensor_presence.presence()
        if pos_front(presence).value:
            await bulb.set_power(True)
        if neg_front(presence).value:
            await bulb.set_power(False)
        await asyncio.sleep(0)


async def run() -> None:
    """Create main task."""
    done, _ = await asyncio.wait(
        [
            asyncio.create_task(deconz_ws.task()),
            asyncio.create_task(bot.task()),
            asyncio.create_task(sensor1.task()),
            asyncio.create_task(sensor_presence.task()),
            asyncio.create_task(bulb.run()),
            asyncio.create_task(_run()),
        ],
        return_when=asyncio.FIRST_EXCEPTION,
    )
    try:
        _ = [d.result() for d in done]
    except BaseException:  # pylint: disable=broad-except
        logger.exception(
            "Необработанное исключение, программа заканчивает выполнение",
        )


def main() -> None:
    """Entry point."""
    asyncio.run(run(), debug=settings.debug)


if __name__ == "__main__":
    main()
