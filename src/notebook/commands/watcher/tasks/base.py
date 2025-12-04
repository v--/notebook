import abc
from datetime import datetime
from typing import TYPE_CHECKING

import loguru

from ..trigger import TaskTrigger


if TYPE_CHECKING:
    from .runner import TaskRunner


class Task(abc.ABC):
    task: TaskTrigger
    base_logger: loguru.Logger
    sublogger: loguru.Logger
    reason: str
    created: datetime

    def __init__(self, trigger: TaskTrigger, reason: str, base_logger: loguru.Logger) -> None:
        self.trigger = trigger
        self.reason = reason
        self.base_logger = base_logger
        self.sublogger = self.create_sublogger(base_logger)
        self.created = datetime.now()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Task):
            return NotImplemented

        return self.trigger == other.trigger

    def __hash__(self) -> int:
        return hash(self.trigger)

    @abc.abstractmethod
    def create_sublogger(self, base_logger: loguru.Logger) -> loguru.Logger:
        ...

    @abc.abstractmethod
    async def build(self, runner: TaskRunner) -> None:
        ...

    @abc.abstractmethod
    async def clean(self, runner: TaskRunner) -> None:
        ...
