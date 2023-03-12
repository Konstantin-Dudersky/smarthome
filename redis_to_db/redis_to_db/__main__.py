import asyncio
import logging

from enum import StrEnum, auto
from db.data.database import Database
from db.connection_string import ConnectionString
from db.data.crud import CrudRows
from db.data.models import Row
from shared.logger import Logger
from shared.redis_subscriber import RedisSubscriber
from shared.settings import SettingsStore
from shared.tasks_runner import TasksRunner

from .message_to_db_rows import message_to_db_rows


class Subscriptions(StrEnum):
    db = auto()


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
redis_subs.add_subs(Subscriptions.db, None)


database = Database(
    conn_str=ConnectionString(
        user=settings.db_user,
        password=settings.db_password,
        host=settings.db_host,
        port=settings.db_port,
        database="db_data",
    ),
)


async def __task() -> None:
    while True:
        while True:
            try:
                msg = redis_subs[Subscriptions.db].pop()
            except IndexError:
                break
            async with database.create_session(Row) as session:
                crud = CrudRows(session, "raw")
                rows = message_to_db_rows(msg)
                await crud.create_many(rows)
                await session.commit()
        await asyncio.sleep(5)


runner.add_task("test", __task())


def main() -> None:
    """Entry point."""
    asyncio.run(runner())


if __name__ == "__main__":
    main()
