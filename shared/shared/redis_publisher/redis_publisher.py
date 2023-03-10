import asyncio
from ipaddress import IPv4Address
from typing import cast

from redis.asyncio import Redis

from shared.simple_deque import ISimpleDequePop, ISimpleDequeAppend, SimpleDeque
from shared.tasks_runner import ITaskRunnerAdd


class RedisPublisher(object):
    def __init__(
        self,
        host: IPv4Address,
        port: int,
        runner: ITaskRunnerAdd,
    ):
        self.__client: Redis[str] = Redis(
            host=str(host),
            port=port,
        )
        self.__messagebus: ISimpleDequePop = SimpleDeque()
        runner.add_task(type(self).__name__, self.__task())

    @property
    def messages(self) -> ISimpleDequeAppend:
        return cast(ISimpleDequeAppend, self.__messagebus)

    async def __task(self) -> None:
        while True:
            try:
                msg: str = self.__messagebus.pop()
            except IndexError:
                await asyncio.sleep(0.1)
                continue
            await self.__client.publish("test_channel", msg)
