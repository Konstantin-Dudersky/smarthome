"""Main script for server."""

import asyncio

from .deconz import Websocket
from .deconz import sensors

deconz_ws = Websocket()
sensor1 = sensors.OpenClose(7, deconz_ws)


async def run() -> None:
    """Create main task."""
    await asyncio.wait(
        [
            asyncio.create_task(deconz_ws.run()),
            asyncio.create_task(sensor1.run()),
        ],
    )


def main() -> None:
    """Entry point."""
    asyncio.run(run(), debug=True)


if __name__ == "__main__":
    main()
