import pathlib
from enum import IntEnum, auto
from typing import NamedTuple


class TaskTriggerKind(IntEnum):
    BUILD = auto()
    CLEAN = auto()


class TaskTrigger(NamedTuple):
    kind: TaskTriggerKind
    path: pathlib.Path
