"""API для доступа к устройствам."""

from fastapi import APIRouter

from src.devices.main import bulb

router = APIRouter(
    prefix="/api/devices",
    tags=["scanner"],
)


@router.get("/")
async def get() -> None:
    """Получить информацию от сканера."""
    return


@router.get("/yeelight/{device_id}")
async def get_yeelight(
    device_id: str,
):
    return await bulb.get_power()
