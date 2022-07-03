"""Devices."""

import asyncio

from src.deconz import Websocket
from src.deconz import sensors
from src.yeelight import Bulb
from src.base import logic
from src.utils.logger import LoggerLevel, get_logger

logger = get_logger(__name__, LoggerLevel.INFO)

deconz_ws = Websocket()
sensor_open_close = sensors.OpenClose(2, deconz_ws)
sensor_presence = sensors.Presence(3, deconz_ws, 1)
sensor_light_level = sensors.LightLevel(4, deconz_ws)
bulb = Bulb("192.168.101.20")


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
    sensor_open_close.task(),
    sensor_presence.task(),
    sensor_light_level.task(),
    bulb.task(),
    _run(),
]
