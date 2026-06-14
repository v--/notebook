import abc
from datetime import datetime
from typing import TYPE_CHECKING


if TYPE_CHECKING:

    from notebook.commands.watcher.trigger import TaskTrigger

    from .runner import TaskRunner


class Task(abc.ABC):
    task: TaskTrigger
    reason: str
    created: datetime

    def __init__(self, trigger: TaskTrigger, reason: str) -> None:
        self.trigger = trigger
        self.reason = reason
        self.created = datetime.now()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Task):
            return NotImplemented

        return self.trigger == other.trigger

    def __hash__(self) -> int:
        return hash(self.trigger)

    @abc.abstractmethod
    async def build(self, runner: TaskRunner) -> None:
        ...

    @abc.abstractmethod
    async def clean(self, runner: TaskRunner) -> None:
        ...
