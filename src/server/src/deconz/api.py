"""Чтение данных REST API."""

import httpx

from src.utils.logger import get_logger, LoggerLevel
from src.utils.settings import settings

from .models import ConfigModel


logger = get_logger(__name__)
logger.setLevel(LoggerLevel.INFO)

DECONZ_REST_URL = (
    f"http://{settings.deconz_ip}:{settings.deconz_rest_port}"
    f"/api/{settings.deconz_api_key}"
)


async def _base_query(endpoint: str) -> httpx.Response | None:
    """Базовый запрос."""
    async with httpx.AsyncClient() as http:
        try:
            return await http.get(f"{DECONZ_REST_URL}{endpoint}")
        except httpx.ConnectError as exc:
            logger.exception("Ошибка выполнения запроса: %s", exc.request)
            return None


# configuration ---------------------------------------------------------------


async def get_config() -> ConfigModel | None:
    """Return the current gateway configuration."""
    config = await _base_query("/config")
    if config is None:
        return None
    return ConfigModel(**config.json())


# sensors ---------------------------------------------------------------------


async def get_sensor(sensor_id: int) -> httpx.Response | None:
    """Return the sensor with the specified id."""
    return await _base_query(f"/sensors/{sensor_id}")
