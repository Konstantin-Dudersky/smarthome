from typing import Coroutine
import pydantic
import pytest

from driver_deconz.deconz.api import Api
from shared.settings import SettingsSchema, SettingsStore
from shared.tasks_runner import TasksRunner


@pytest.fixture
def settings() -> SettingsSchema:
    return SettingsStore("../.env").settings


@pytest.fixture
def deconz_api_task(settings: SettingsSchema) -> Coroutine[None, None, None]:
    runner = TasksRunner()
    Api(
        host=settings.deconz_hub_host,
        port_api=settings.deconz_hub_port_api,
        api_key=pydantic.SecretStr(""),
        runner=runner,
    )
    return runner._TaskRunner__coros[0]  # type: ignore
