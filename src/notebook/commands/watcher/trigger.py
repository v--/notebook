from enum import IntEnum, auto
from typing import TYPE_CHECKING, NamedTuple


if TYPE_CHECKING:
    import pathlib


class TaskTriggerKind(IntEnum):
    BUILD = auto()
    CLEAN = auto()


class TaskTrigger(NamedTuple):
    kind: TaskTriggerKind
    path: pathlib.Path
