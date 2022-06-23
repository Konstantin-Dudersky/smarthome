"""Main script for server."""

import asyncio

from .deconz import Websocket
from .deconz import sensors

deconz_ws = Websocket()
sensor1 = sensors.OpenClose()


# async def run():
#     asyncio.create_task(deconz_ws.run())


async def run() -> None:
    await asyncio.wait(
        [
            deconz_ws.run(),
            sensor1.run(),
        ],
    )


# async def run():
#     while True:
#         await deconz_ws.run()

def main() -> None:
    asyncio.run(run(), debug=True)
