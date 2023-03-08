from shared.redis_publisher import RedisPublisher
from shared.settings import SettingsSchema


def test_publisher(settings: SettingsSchema) -> None:
    rp = RedisPublisher(
        host=settings.redis_host,
        port=settings.redis_port,
    )
