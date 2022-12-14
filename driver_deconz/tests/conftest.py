import ipaddress

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
        host=ipaddress.IPv4Address("127.0.0.1"),
        port_api=8000,
        api_key=pydantic.SecretStr(""),
    )
