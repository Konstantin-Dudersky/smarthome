import pytest

from shared.settings import SettingsSchema, SettingsStore


@pytest.fixture
def settings() -> SettingsSchema:
    return SettingsStore("../.env").settings
