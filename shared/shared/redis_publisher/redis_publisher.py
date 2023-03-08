import asyncio

from ipaddress import IPv4Address
from typing import Coroutine, Iterable

from redis.asyncio import Redis

from shared.messagebus import MessagebusProtocolPop
from shared.async_tasks import TasksProtocol


class RedisPublisher(TasksProtocol):
    def __init__(
        self,
        host: IPv4Address,
        port: int,
        messagebus: MessagebusProtocolPop,
    ):
        self.__client: Redis[str] = Redis(
            host=str(host),
            port=port,
        )
        self.__messagebus = messagebus

    @property
    def async_tasks(self) -> Iterable[Coroutine[None, None, None]]:
        """Перечень задач для запуска."""
        return {self.__task()}

    async def __task(self) -> None:
        while True:
            try:
                msg: str = self.__messagebus.pop()
            except IndexError:
                await asyncio.sleep(0.1)
                continue
            await self.__client.publish("test_channel", msg)
