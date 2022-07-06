"""Devices."""

import asyncio
from typing import Any, Coroutine

from src.deconz import Websocket
from src.deconz import sensors
from src.yeelight import Bulb
from src.base import logic
from src.utils.logger import LoggerLevel, get_logger

logger = get_logger(__name__, LoggerLevel.INFO)

tasks1: list[Coroutine[Any, Any, None]] = []

deconz_ws = Websocket()
sensor_open_close = sensors.OpenClose(2, deconz_ws, atasks=tasks1)
sensor_presence = sensors.Presence(3, deconz_ws, atasks=tasks1, update_rate=1)
sensor_light_level = sensors.LightLevel(4, deconz_ws, atasks=tasks1)
bulb = Bulb("192.168.101.20")
humidity = sensors.Humidity(11, deconz_ws, atasks=tasks1)


async def _run() -> None:
    pos_front = logic.PosFront()
    neg_front = logic.NegFront()
    while True:
        presence = await sensor_presence.presence()
        if pos_front(presence).value:
            await bulb.set_power(True, duration=1000)
        if neg_front(presence).value:
            await bulb.set_power(False, duration=10000)
        await asyncio.sleep(0)


tasks = [
    deconz_ws.task(),
    bulb.task(),
    _run(),
]

tasks.extend(tasks1)
