"""Main script for server."""

import asyncio

from src.utils.settings import settings
from src.utils.telegram import bot
from src.utils.logger import LoggerLevel, get_logger

from .api import api_task
from .devices import tasks as devices_tasks


log = get_logger(__name__, LoggerLevel.INFO)


async def run() -> None:
    """Create main task."""
    done, _ = await asyncio.wait(
        [
            *[asyncio.create_task(t) for t in devices_tasks],
            asyncio.create_task(bot.task()),
            asyncio.create_task(api_task()),
        ],
        return_when=asyncio.FIRST_EXCEPTION,
    )
    try:
        _ = [d.result() for d in done]
    except BaseException:  # pylint: disable=broad-except
        log.exception(
            "Необработанное исключение, программа заканчивает выполнение",
        )


def main() -> None:
    """Entry point."""
    asyncio.run(run(), debug=settings.debug)


if __name__ == "__main__":
    main()
