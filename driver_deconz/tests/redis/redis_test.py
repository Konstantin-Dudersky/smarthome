import asyncio

from redis.asyncio import Redis

from shared.settings import SettingsSchema


def test_publish(settings: SettingsSchema):
    redis_client: Redis[str] = Redis(
        host=str(settings.redis_host),
        port=settings.redis_port,
    )

    async def publish():
        await redis_client.publish("test_channel", "Hello from python")

    asyncio.run(publish())
