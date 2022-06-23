"""Модели Pydantic."""

from datetime import datetime
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
