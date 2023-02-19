import asyncio

import redis.asyncio as redis


def test_redis():
    r = redis.Redis(host="192.168.101.10")

    async def publish():
        await r.publish("test_channel", "Hello from python")

    asyncio.run(publish())
