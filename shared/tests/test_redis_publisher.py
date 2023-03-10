from shared.redis_publisher import RedisPublisher
from shared.settings import SettingsSchema
from shared.tasks_runner import TasksRunner


def test_publisher(settings: SettingsSchema) -> None:
    runner = TasksRunner()
    RedisPublisher(
        host=settings.redis_host,
        port=settings.redis_port,
        runner=runner,
    )
