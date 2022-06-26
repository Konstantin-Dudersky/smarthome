"""Main script for server."""

import asyncio
from cmath import log

from src.base.types import Di, Qual

from .base import logic

from .deconz import Websocket
from .deconz import sensors

from .yeelight import Bulb

deconz_ws = Websocket()
sensor1 = sensors.OpenClose(7, deconz_ws)
bulb = Bulb("192.168.101.20")


async def _run() -> None:
    pos_front = logic.PosFront()
    neg_front = logic.NegFront()
    while True:
        opened = await sensor1.opened()
        if pos_front(opened).value:
            await bulb.set_power(True)
        if neg_front(opened).value:
            await bulb.set_power(False)
        await asyncio.sleep(0)


async def run() -> None:
    """Create main task."""
    await asyncio.wait(
        [
            asyncio.create_task(deconz_ws.run()),
            asyncio.create_task(sensor1.run()),
            asyncio.create_task(bulb.run()),
            asyncio.create_task(_run()),
        ],
        return_when=asyncio.FIRST_EXCEPTION,
    )


def main() -> None:
    """Entry point."""
    asyncio.run(run(), debug=True)


if __name__ == "__main__":
    main()
