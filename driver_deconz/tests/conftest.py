import pydantic
import pytest

from driver_deconz.deconz.api import Api
from shared.settings import SettingsSchema, SettingsStore


@pytest.fixture
def settings() -> SettingsSchema:
    return SettingsStore("../.env").settings


@pytest.fixture
def deconz_api(settings: SettingsSchema) -> Api:
    return Api(
        host=settings.deconz_hub_host,
        port_api=settings.deconz_hub_port_api,
        api_key=pydantic.SecretStr(""),
    )
