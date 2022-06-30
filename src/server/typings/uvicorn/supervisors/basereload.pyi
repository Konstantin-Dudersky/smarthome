"""
This type stub file was generated by pyright.
"""

from pathlib import Path
from socket import socket
from types import FrameType
from typing import Callable, Iterator, List, Optional
from uvicorn.config import Config

HANDLED_SIGNALS = ...
logger = ...
class BaseReload:
    def __init__(self, config: Config, target: Callable[[Optional[List[socket]]], None], sockets: List[socket]) -> None:
        ...
    
    def signal_handler(self, sig: int, frame: Optional[FrameType]) -> None:
        """
        A signal handler that is registered with the parent process.
        """
        ...
    
    def run(self) -> None:
        ...
    
    def pause(self) -> None:
        ...
    
    def __iter__(self) -> Iterator[Optional[List[Path]]]:
        ...
    
    def __next__(self) -> Optional[List[Path]]:
        ...
    
    def startup(self) -> None:
        ...
    
    def restart(self) -> None:
        ...
    
    def shutdown(self) -> None:
        ...
    
    def should_restart(self) -> Optional[List[Path]]:
        ...
    


