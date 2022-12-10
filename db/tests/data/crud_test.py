import asyncio

import arrow
import db


model = db.data.models.Row

rows_to_save = (
    model(
        ts=arrow.utcnow(),
        entity=1,
        attr="attribute",
        value=10,
        agg=db.data.models.AggEnum.curr,
        status=db.data.models.StatusEnum.bad,
        aggts=arrow.utcnow(),
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
        agg=db.data.models.AggEnum.curr,
        status=db.data.models.StatusEnum.bad,
        aggts=arrow.utcnow(),
        aggnext=None,
    ),
)


def test_create_one(database: db.data.Database) -> None:
    async def run() -> None:

        async with database.create_session(model) as session:
            crud = db.data.crud.CrudRows(session, "raw")
            await crud.delete_all()
            await crud.create_one(rows_to_save[0])

    asyncio.run(run())

    assert True


def test_create_one_read_all(database: db.data.Database) -> None:
    async def run() -> None:

        async with database.create_session(model) as session:
            crud = db.data.crud.CrudRows(session, "raw")
            for row in rows_to_save:
                print("test row: {0}".format(row))
                await crud.delete_all()
                await crud.create_one(row)
                load_rows = await crud.read_all()
                assert row == load_rows[0]

    asyncio.run(run())


def test_read_all(database: db.data.Database) -> None:
    async def run() -> None:
        async with database.create_session(model) as session:
            result = await db.data.crud.CrudRows(session, "raw").read_all()
            print(result)

    asyncio.run(run())

    assert False
