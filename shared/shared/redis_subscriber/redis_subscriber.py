# pyright: reportUnknownMemberType=false

import asyncio
import logging
from ipaddress import IPv4Address
from typing import Any

from redis.asyncio import Redis

from shared.tasks_runner import ITaskRunnerAdd
from shared.messages import OpenCloseSensor, BaseMessage

from .subs_collection import SubsCollection
from ..simple_deque import ISimpleDequePop

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class RedisSubscriber(object):
    def __init__(
        self,
        host: IPv4Address,
        port: int,
        runner: ITaskRunnerAdd,
    ) -> None:
        runner.add_task("RedisSubscriber", self.__task())

        self.__client: Redis[str] = Redis(
            host=str(host),
            port=port,
            decode_responses=True,
        )
        self.__subs = SubsCollection()

    async def __task(self) -> None:
        async with self.__client.pubsub() as pubsub:
            await pubsub.subscribe("test_channel")
            while True:
                message: dict[str, Any] | None = await pubsub.get_message(
                    ignore_subscribe_messages=True,
                )
                if message is not None:
                    log.debug("message received: {0}".format(message))
                    self.__process_message(message["data"])
                await asyncio.sleep(0.1)

    def __process_message(self, message: str) -> None:
        base_message = BaseMessage.parse_raw(message)
        full_message = OpenCloseSensor.parse_raw(message)
        self.__subs.new_message(full_message.entity_id, full_message)

    def add_subs(self, subs_name: str, entity_id: str | None) -> None:
        self.__subs.add_subs(subs_name, entity_id)

    def __getitem__(self, subs_name: str) -> ISimpleDequePop[BaseMessage]:
        return self.__subs[subs_name]
