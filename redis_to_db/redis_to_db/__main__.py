import asyncio
import logging

from shared.logger import Logger
from shared.redis_subscriber import RedisSubscriber
from shared.settings import SettingsStore
from shared.tasks_runner import TasksRunner

Logger(output_to_console=True)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

settings = SettingsStore("../.env").settings

runner = TasksRunner()

redis_subs = RedisSubscriber(
    host=settings.redis_host,
    port=settings.redis_port,
    runner=runner,
)


def main() -> None:
    """Entry point."""
    asyncio.run(runner())


if __name__ == "__main__":
    main()
