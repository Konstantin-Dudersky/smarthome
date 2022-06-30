"""
This type stub file was generated by pyright.
"""

import asyncio
import logging
import sys
from typing import Callable, List, Optional, TYPE_CHECKING, Tuple
from uvicorn.config import Config
from uvicorn.protocols.http.flow_control import FlowControl
from uvicorn.server import ServerState
from asgiref.typing import ASGI3Application, ASGIReceiveEvent, ASGISendEvent, HTTPScope

if sys.version_info < (3, 8):
    ...
else:
    ...
if TYPE_CHECKING:
    ...
HEADER_RE = ...
HEADER_VALUE_RE = ...
STATUS_LINE = ...
class HttpToolsProtocol(asyncio.Protocol):
    def __init__(self, config: Config, server_state: ServerState, _loop: Optional[asyncio.AbstractEventLoop] = ...) -> None:
        ...
    
    def connection_made(self, transport: asyncio.Transport) -> None:
        ...
    
    def connection_lost(self, exc: Optional[Exception]) -> None:
        ...
    
    def eof_received(self) -> None:
        ...
    
    def data_received(self, data: bytes) -> None:
        ...
    
    def handle_upgrade(self) -> None:
        ...
    
    def send_400_response(self, msg: str) -> None:
        ...
    
    def on_message_begin(self) -> None:
        ...
    
    def on_url(self, url: bytes) -> None:
        ...
    
    def on_header(self, name: bytes, value: bytes) -> None:
        ...
    
    def on_headers_complete(self) -> None:
        ...
    
    def on_body(self, body: bytes) -> None:
        ...
    
    def on_message_complete(self) -> None:
        ...
    
    def on_response_complete(self) -> None:
        ...
    
    def shutdown(self) -> None:
        """
        Called by the server to commence a graceful shutdown.
        """
        ...
    
    def pause_writing(self) -> None:
        """
        Called by the transport when the write buffer exceeds the high water mark.
        """
        ...
    
    def resume_writing(self) -> None:
        """
        Called by the transport when the write buffer drops below the low water mark.
        """
        ...
    
    def timeout_keep_alive_handler(self) -> None:
        """
        Called on a keep-alive connection if no new data is received after a short
        delay.
        """
        ...
    


class RequestResponseCycle:
    def __init__(self, scope: HTTPScope, transport: asyncio.Transport, flow: FlowControl, logger: logging.Logger, access_logger: logging.Logger, access_log: bool, default_headers: List[Tuple[bytes, bytes]], message_event: asyncio.Event, expect_100_continue: bool, keep_alive: bool, on_response: Callable[..., None]) -> None:
        ...
    
    async def run_asgi(self, app: ASGI3Application) -> None:
        ...
    
    async def send_500_response(self) -> None:
        ...
    
    async def send(self, message: ASGISendEvent) -> None:
        ...
    
    async def receive(self) -> ASGIReceiveEvent:
        ...
    


