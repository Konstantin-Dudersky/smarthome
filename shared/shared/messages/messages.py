from .base_message import BaseMessage
from .register_message import register_message


@register_message
class OpenCloseSensor(BaseMessage):
    """Датчик с двумя состояниями."""

    opened: bool


@register_message
class TemperatureSensor(BaseMessage):
    """Датчик температуры."""

    temperature: float


@register_message
class HumiditySensor(BaseMessage):
    """Датчик температуры."""

    humidity: float


@register_message
class PressureSensor(BaseMessage):
    """Датчик температуры."""

    pressure: float


@register_message
class PresenceSensor(BaseMessage):
    """Датчик присутствия."""

    presence: bool


@register_message
class LightLevel(BaseMessage):
    """Датчик освещенности."""

    lux: float
