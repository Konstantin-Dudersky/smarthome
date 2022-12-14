import asyncio
from pytest_httpx import HTTPXMock


from driver_deconz.deconz.api import Api


def test_api(httpx_mock: HTTPXMock, deconz_api: Api) -> None:
    httpx_mock.add_response(
        json=[{"key1": "value1", "key2": "value2"}],
    )

    async def run():
        task = list(deconz_api.async_tasks)[0]
        try:
            await asyncio.wait_for(task, 1.0)
        except asyncio.TimeoutError:
            pass

    asyncio.run(run())

    print(deconz_api.full_state)

    assert True
