"""
This type stub file was generated by pyright.
"""

from pathlib import Path
from socket import socket
from typing import Callable, List, Optional
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload

class FileFilter:
    def __init__(self, config: Config) -> None:
        ...
    
    def __call__(self, path: Path) -> bool:
        ...
    


class WatchFilesReload(BaseReload):
    def __init__(self, config: Config, target: Callable[[Optional[List[socket]]], None], sockets: List[socket]) -> None:
        ...
    
    def should_restart(self) -> Optional[List[Path]]:
        ...
    


