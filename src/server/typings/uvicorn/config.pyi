"""
This type stub file was generated by pyright.
"""

import asyncio
import os
import socket
import ssl
import sys
from pathlib import Path
from typing import Any, Awaitable, Callable, Dict, List, Literal, Optional, TYPE_CHECKING, Tuple, Type, Union
from asgiref.typing import ASGIApplication

if sys.version_info < (3, 8):
    ...
else:
    ...
if TYPE_CHECKING:
    ...
HTTPProtocolType = Literal["auto", "h11", "httptools"]
WSProtocolType = Literal["auto", "none", "websockets", "wsproto"]
LifespanType = Literal["auto", "on", "off"]
LoopSetupType = Literal["none", "auto", "asyncio", "uvloop"]
InterfaceType = Literal["auto", "asgi3", "asgi2", "wsgi"]
LOG_LEVELS: Dict[str, int] = ...
HTTP_PROTOCOLS: Dict[HTTPProtocolType, str] = ...
WS_PROTOCOLS: Dict[WSProtocolType, Optional[str]] = ...
LIFESPAN: Dict[LifespanType, str] = ...
LOOP_SETUPS: Dict[LoopSetupType, Optional[str]] = ...
INTERFACES: List[InterfaceType] = ...
SSL_PROTOCOL_VERSION: int = ...
LOGGING_CONFIG: Dict[str, Any] = ...
logger = ...
def create_ssl_context(certfile: Union[str, os.PathLike], keyfile: Optional[Union[str, os.PathLike]], password: Optional[str], ssl_version: int, cert_reqs: int, ca_certs: Optional[Union[str, os.PathLike]], ciphers: Optional[str]) -> ssl.SSLContext:
    ...

def is_dir(path: Path) -> bool:
    ...

def resolve_reload_patterns(patterns_list: List[str], directories_list: List[str]) -> Tuple[List[str], List[Path]]:
    ...

class Config:
    def __init__(self, app: Union[ASGIApplication, Callable, str], host: str = ..., port: int = ..., uds: Optional[str] = ..., fd: Optional[int] = ..., loop: LoopSetupType = ..., http: Union[Type[asyncio.Protocol], HTTPProtocolType] = ..., ws: Union[Type[asyncio.Protocol], WSProtocolType] = ..., ws_max_size: int = ..., ws_ping_interval: Optional[float] = ..., ws_ping_timeout: Optional[float] = ..., ws_per_message_deflate: Optional[bool] = ..., lifespan: LifespanType = ..., env_file: Optional[Union[str, os.PathLike]] = ..., log_config: Optional[Union[Dict[str, Any], str]] = ..., log_level: Optional[Union[str, int]] = ..., access_log: bool = ..., use_colors: Optional[bool] = ..., interface: InterfaceType = ..., debug: bool = ..., reload: bool = ..., reload_dirs: Optional[Union[List[str], str]] = ..., reload_delay: Optional[float] = ..., reload_includes: Optional[Union[List[str], str]] = ..., reload_excludes: Optional[Union[List[str], str]] = ..., workers: Optional[int] = ..., proxy_headers: bool = ..., server_header: bool = ..., date_header: bool = ..., forwarded_allow_ips: Optional[str] = ..., root_path: str = ..., limit_concurrency: Optional[int] = ..., limit_max_requests: Optional[int] = ..., backlog: int = ..., timeout_keep_alive: int = ..., timeout_notify: int = ..., callback_notify: Callable[..., Awaitable[None]] = ..., ssl_keyfile: Optional[str] = ..., ssl_certfile: Optional[Union[str, os.PathLike]] = ..., ssl_keyfile_password: Optional[str] = ..., ssl_version: int = ..., ssl_cert_reqs: int = ..., ssl_ca_certs: Optional[str] = ..., ssl_ciphers: str = ..., headers: Optional[List[Tuple[str, str]]] = ..., factory: bool = ..., h11_max_incomplete_event_size: int = ...) -> None:
        ...
    
    @property
    def asgi_version(self) -> Literal["2.0", "3.0"]:
        ...
    
    @property
    def is_ssl(self) -> bool:
        ...
    
    @property
    def use_subprocess(self) -> bool:
        ...
    
    def configure_logging(self) -> None:
        ...
    
    def load(self) -> None:
        ...
    
    def setup_event_loop(self) -> None:
        ...
    
    def bind_socket(self) -> socket.socket:
        ...
    
    @property
    def should_reload(self) -> bool:
        ...
    


