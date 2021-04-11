from __future__ import annotations

from enum import IntEnum
from typing import Any, TypedDict

from pyclig.color.detection import ColorDetection


class HandlerVerbosity(IntEnum):
    Quiet = 0
    Normal = 1
    Verbose = 2


class ColorEnabled(IntEnum):
    Auto = 0
    Enabled = 1
    Disabled = 2


class Options(TypedDict):
    verbosity: HandlerVerbosity
    json: bool
    color: ColorEnabled


class HandlerBuilder:
    _output_config: dict
    _messaging_config: dict

    _output_options: Options
    _messaging_options: Options

    def __init__(self, output_config: Options, messaging_config: Options) -> None:
        self._output_options = output_config
        self._messaging_options = messaging_config
        self._color_detector = ColorDetection(disable_color=False)
