"""
This type stub file was generated by pyright.
"""

import logging
import sys
from typing import Literal, Optional

if sys.version_info < (3, 8):
    ...
else:
    ...
TRACE_LOG_LEVEL = ...
class ColourizedFormatter(logging.Formatter):
    """
    A custom log formatter class that:

    * Outputs the LOG_LEVEL with an appropriate color.
    * If a log call includes an `extras={"color_message": ...}` it will be used
      for formatting the output, instead of the plain text message.
    """
    level_name_colors = ...
    def __init__(self, fmt: Optional[str] = ..., datefmt: Optional[str] = ..., style: Literal["%", "{", "$"] = ..., use_colors: Optional[bool] = ...) -> None:
        ...
    
    def color_level_name(self, level_name: str, level_no: int) -> str:
        ...
    
    def should_use_colors(self) -> bool:
        ...
    
    def formatMessage(self, record: logging.LogRecord) -> str:
        ...
    


class DefaultFormatter(ColourizedFormatter):
    def should_use_colors(self) -> bool:
        ...
    


class AccessFormatter(ColourizedFormatter):
    status_code_colours = ...
    def get_status_code(self, status_code: int) -> str:
        ...
    
    def formatMessage(self, record: logging.LogRecord) -> str:
        ...
    


