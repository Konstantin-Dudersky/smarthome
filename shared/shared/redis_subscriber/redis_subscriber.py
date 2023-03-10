import asyncio
import logging
from ipaddress import IPv4Address

from redis.asyncio import Redis

from shared.tasks_runner import ITaskRunnerAdd

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class RedisSubscriber(object):
    def __init__(
        self,
        host: IPv4Address,
        port: int,
        runner: ITaskRunnerAdd,
    ) -> None:
        self.__client: Redis[str] = Redis(
            host=str(host),
            port=port,
        )
        runner.add_task("RedisSubscriber", self.__task())

    async def __task(self) -> None:
        async with self.__client.pubsub() as pubsub:
            await pubsub.subscribe("test_channel")
            while True:
                message = await pubsub.get_message(
                    ignore_subscribe_messages=True,
                )
                if message is not None:
                    log.debug(message)
                await asyncio.sleep(0.1)
