import asyncio

import arrow
import db

from db.data.crud.const import CHUNK_SIZE

model = db.data.models.Row

rows_to_save: tuple[model, ...] = (
    model(
        ts=arrow.utcnow(),
        entity=1,
        attr="attribute",
        value=None,
        agg=db.data.models.AggEnum.curr,
        status=db.data.models.StatusEnum.bad,
        aggts=None,
        aggnext=(
            db.data.models.AggEnum.first,
            db.data.models.AggEnum.inc,
        ),
    ),
    model(
        ts=arrow.utcnow(),
        entity=1,
        attr="attribute",
        value=10,
        agg=db.data.models.AggEnum.first,
        status=db.data.models.StatusEnum.good,
        aggts=arrow.utcnow(),
        aggnext=None,
    ),
    model(
        ts=arrow.utcnow(),
        entity=1,
        attr="attribute",
        value=10,
        agg=db.data.models.AggEnum.inc,
        status=db.data.models.StatusEnum.uncertain,
        aggts=arrow.utcnow(),
        aggnext=None,
    ),
)


def test_create_one(database: db.data.Database) -> None:
    async def run() -> None:

        async with database.create_session(model) as session:
            crud = db.data.crud.crud_rows.CrudRows(session, "raw")
            await crud.delete_all()
            await crud.create_one(rows_to_save[0])

    asyncio.run(run())

    assert True


def test_create_many(database: db.data.Database) -> None:
    async def run() -> None:

        async with database.create_session(model) as session:
            crud = db.data.crud.crud_rows.CrudRows(session, "raw")
            await crud.delete_all()
            await crud.create_many(rows_to_save)

    asyncio.run(run())

    assert True


def test_create_many_large(database: db.data.Database) -> None:
    async def run() -> None:

        import copy

        async with database.create_session(model) as session:
            entity_index = 0
            rows_to_save_large: list[model] = []
            value = 3 * (CHUNK_SIZE / 8) / len(rows_to_save)
            for _ in range(int(value)):
                rows = copy.deepcopy(rows_to_save)
                for row in rows:
                    row.entity = entity_index
                    entity_index += 1
                rows_to_save_large.extend(rows)
            crud = db.data.crud.crud_rows.CrudRows(session, "raw")
            await crud.delete_all()
            await crud.create_many(rows_to_save_large)

    asyncio.run(run())

    assert True


def test_create_one_read_all(database: db.data.Database) -> None:
    async def run() -> None:

        async with database.create_session(model) as session:
            crud = db.data.crud.crud_rows.CrudRows(session, "raw")
            for row in rows_to_save:
                print("test row: {0}".format(row))
                await crud.delete_all()
                await crud.create_one(row)
                load_rows = await crud.read_all()
                assert row == load_rows[0]

    asyncio.run(run())
