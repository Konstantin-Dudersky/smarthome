import asyncio
import logging

import arrow
from enum import StrEnum, auto
from db.data.database import Database
from db.connection_string import ConnectionString
from db.data.crud import CrudRows
from db.data.models import Row, AggEnum
from shared.logger import Logger
from shared.redis_subscriber import RedisSubscriber
from shared.settings import SettingsStore
from shared.tasks_runner import TasksRunner

from .message_to_db_rows import message_to_db_rows


class Subs(StrEnum):
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
redis_subs.add_subs(Subs.db, "open_close")


database = Database(
    conn_str=ConnectionString(
        driver="postgresql",
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
                msg = redis_subs[Subs.db].pop()
            except IndexError:
                break
            log.warning(msg)
            async with database.create_session(Row) as session:
                crud = CrudRows(session, "raw")
                rows = message_to_db_rows(msg)
                await crud.create_many(rows)
        await asyncio.sleep(5)


runner.add_task("test", __task())


def main() -> None:
    """Entry point."""
    asyncio.run(runner())


if __name__ == "__main__":
    main()
