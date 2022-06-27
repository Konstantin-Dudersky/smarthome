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


class WsStateOpenClose(BaseModel):
    """state для ZHAOpenClose."""

    lastupdated: datetime
    opened: bool = Field(..., alias="open")


class WsMsg(BaseModel):
    """Базовое сообщение."""

    event: WsEvents = Field(..., alias="e")
    resource_id: int = Field(..., alias="id")
    resource: WsResources = Field(..., alias="r")
    msg_type: WsTypes = Field(..., alias="t")
    uniqueid: str


class WsMsgOpenClose(WsMsg):
    """Сообщение 1."""

    state: WsStateOpenClose


class WsMsgWithoutState(WsMsg):
    """Сообщение 2."""

    attr: WsAttr


# ZHAOpenClose ----------------------------------------------------------------


class SensorOpenCloseConfig(BaseModel):
    """Sensor config."""

    battery: int
    on: bool
    reachable: bool
    temperature: int


class SensorOpenCloseState(BaseModel):
    """Состояние датчика открытия/закрытия."""

    lastupdated: datetime
    opened: bool = Field(..., alias="open")


class SensorOpenClose(BaseModel):
    """Датчик открытия/закрытия."""

    config: SensorOpenCloseConfig
    ep: int
    etag: str
    lastannounced: datetime | None
    lastseen: datetime
    manufacturername: str
    modelid: str
    name: str
    state: SensorOpenCloseState
    swversion: str
    type_sensor: str = Field(..., alias="type")
    uniqueid: str


# ZHAPresence -----------------------------------------------------------------


class ZHAPresenceConfig(BaseModel):
    """Sensor config."""

    battery: int
    duration: int
    on: bool
    reachable: bool
    temperature: int


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


class WsStatePresence(BaseModel):
    """state для ZHAOpenClose."""

    lastupdated: datetime
    presence: bool


class WsMsgPresence(WsMsg):
    """Сообщение 1."""

    state: WsStatePresence
