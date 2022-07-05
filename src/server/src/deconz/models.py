"""Модели Pydantic."""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ConfigModel(BaseModel):
    """Ответ на config."""

    apiversion: str
    backup: Any
    bridgeid: str
    datastoreversion: str
    devicename: str
    dhcp: bool
    factorynew: bool
    fwversion: str
    gateway: str
    internetservices: Any
    ipaddress: str
    lightlastseeninterval: int
    linkbutton: bool
    localtime: str
    mac: str
    modelid: str
    name: str
    netmask: str
    networkopenduration: int
    panid: int
    portalconnection: str
    portalservices: bool
    portalstate: Any
    proxyaddress: str
    proxyport: int
    replacesbridgeid: Any
    rfconnected: bool
    starterkitid: str
    swupdate: Any
    swupdate2: Any
    swversion: str
    timeformat: str
    timezone: str
    uuid: str
    websocketnotifyall: bool
    websocketport: int
    whitelist: Any
    zigbeechannel: int
    disable_permit_join_auto_off: bool = Field(
        ...,
        alias="disablePermitJoinAutoOff",
    )
    utc: datetime = Field(..., alias="UTC")


# websocket -------------------------------------------------------------------


class WsEvents(Enum):
    """The event type of the message."""

    ADDED = "added"
    CHANGED = "changed"
    DELETED = "deleted"
    SCENE_CALLED = "scene-called"


class WsResources(Enum):
    """The resource type to which the message belongs."""

    GROUPS = "groups"
    LIGHTS = "lights"
    SCENES = "scenes"
    SENSORS = "sensors"


class WsTypes(Enum):
    """The type of the message."""

    EVENT = "event"


class WsAttr(BaseModel):
    """Атрибуты сообщения."""

    resource_id: int = Field(..., alias="id")
    lastannounced: datetime | None
    lastseen: datetime
    manufacturername: str
    modelid: str
    name: str
    swversion: str
    attr_type: str = Field(..., alias="type")
    uniqueid: str


class WsMsg(BaseModel):
    """Базовое сообщение."""

    event: WsEvents = Field(..., alias="e")
    resource_id: int = Field(..., alias="id")
    resource: WsResources = Field(..., alias="r")
    msg_type: WsTypes = Field(..., alias="t")
    uniqueid: str


class WsMsgWithoutState(WsMsg):
    """Сообщение 2."""

    attr: WsAttr


# ZHAOpenClose ----------------------------------------------------------------


class ZHAOpenCloseComfig(BaseModel):
    """Sensor config."""

    battery: int
    on: bool
    reachable: bool
    temperature: int


class ZHAOpenCloseState(BaseModel):
    """Состояние датчика открытия/закрытия."""

    lastupdated: datetime
    opened: bool = Field(..., alias="open")


class ZHAOpenClose(BaseModel):
    """Датчик открытия/закрытия."""

    config: ZHAOpenCloseComfig
    ep: int
    etag: str
    lastannounced: datetime | None
    lastseen: datetime
    manufacturername: str
    modelid: str
    name: str
    state: ZHAOpenCloseState
    swversion: str
    type_sensor: str = Field(..., alias="type")
    uniqueid: str


class ZHAOpenCloseStateWs(BaseModel):
    """state для ZHAOpenClose."""

    lastupdated: datetime
    opened: bool = Field(..., alias="open")


class ZHAOpenCloseWs(WsMsg):
    """Сообщение 1."""

    state: ZHAOpenCloseStateWs


# ZHAPresence -----------------------------------------------------------------


class ZHAPresenceConfig(BaseModel):
    """Sensor config."""

    battery: int
    duration: int
    on: bool
    reachable: bool


class ZHAPresenceState(BaseModel):
    """Состояние датчика открытия/закрытия."""

    lastupdated: datetime
    presence: bool


class ZHAPresence(BaseModel):
    """Датчик присутствия."""

    config: ZHAPresenceConfig
    ep: int
    etag: str
    lastannounced: datetime | None
    lastseen: datetime
    manufacturername: str
    modelid: str
    name: str
    state: ZHAPresenceState
    swversion: str
    type_sensor: str = Field(..., alias="type")
    uniqueid: str


class ZHAPresenceStateWs(BaseModel):
    """state для ZHAOpenClose."""

    lastupdated: datetime
    presence: bool


class ZHAPresenceWs(WsMsg):
    """Сообщение 1."""

    state: ZHAPresenceStateWs


# ZHALightLevel ---------------------------------------------------------------


class ZHALightLevelConfig(BaseModel):
    """Sensor config."""

    battery: int
    on: bool
    reachable: bool
    tholddark: int
    tholdoffset: int


class ZHALightLevelState(BaseModel):
    """Состояние датчика открытия/закрытия."""

    dark: bool
    daylight: bool
    lastupdated: datetime
    lightlevel: int
    lux: int


class ZHALightLevel(BaseModel):
    """Датчик освещенности."""

    config: ZHALightLevelConfig
    ep: int
    etag: str
    lastannounced: datetime | None
    lastseen: datetime
    manufacturername: str
    modelid: str
    name: str
    state: ZHALightLevelState
    swversion: str
    type_sensor: str = Field(..., alias="type")
    uniqueid: str


class ZHALightLevelStateWs(BaseModel):
    """state для ZHAOpenClose."""

    lastupdated: datetime
    presence: bool


class ZHALightLevelWs(WsMsg):
    """Сообщение 1."""

    state: ZHALightLevelStateWs


# ZHAHumidity -----------------------------------------------------------------


class ZHAHumidityConfig(BaseModel):
    """Sensor config."""

    battery: int
    offset: int
    on: bool
    reachable: bool


class ZHAHumidityState(BaseModel):
    """Состояние датчика влажности."""

    humidity: int
    lastupdated: datetime


class ZHAHumidity(BaseModel):
    """Датчик влажности."""

    config: ZHAHumidityConfig
    ep: int
    etag: str
    lastannounced: datetime | None
    lastseen: datetime
    manufacturername: str
    modelid: str
    name: str
    state: ZHAHumidityState
    swversion: str
    type_sensor: str = Field(..., alias="type")
    uniqueid: str
