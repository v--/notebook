from enum import IntEnum, auto
from typing import NamedTuple
lazy import pathlib


class TaskTriggerKind(IntEnum):
    BUILD = auto()
    CLEAN = auto()


class TaskTrigger(NamedTuple):
    kind: TaskTriggerKind
    path: pathlib.Path
