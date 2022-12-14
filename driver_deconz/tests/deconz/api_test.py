import asyncio
import json
from pytest_httpx import HTTPXMock


from driver_deconz.deconz.api import Api


def test_api(httpx_mock: HTTPXMock, deconz_api: Api) -> None:
    with open("tests/deconz/full_state_response.json", "r") as file:
        response = json.load(file)
    httpx_mock.add_response(
        json=response,
    )

    async def run():
        task = list(deconz_api.async_tasks)[0]
        try:
            await asyncio.wait_for(task, 1.0)
        except asyncio.TimeoutError:
            pass

    asyncio.run(run())

    assert response == json.loads(deconz_api.full_state)
