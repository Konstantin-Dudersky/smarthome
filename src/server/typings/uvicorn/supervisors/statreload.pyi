"""
This type stub file was generated by pyright.
"""

from pathlib import Path
from socket import socket
from typing import Callable, Iterator, List, Optional
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload

logger = ...
class StatReload(BaseReload):
    def __init__(self, config: Config, target: Callable[[Optional[List[socket]]], None], sockets: List[socket]) -> None:
        ...
    
    def should_restart(self) -> Optional[List[Path]]:
        ...
    
    def restart(self) -> None:
        ...
    
    def iter_py_files(self) -> Iterator[Path]:
        ...
    


