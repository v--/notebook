import abc
from typing import TYPE_CHECKING

import loguru


if TYPE_CHECKING:
    from .runner import TaskRunner


class WatcherTask(abc.ABC):
    sublogger: 'loguru.Logger'
    out_buffer: int | None

    def __eq__(self, other: object) -> bool:
        return isinstance(other, WatcherTask) and self.command == other.command

    def __hash__(self) -> int:
        return hash(self.command)

    @property
    @abc.abstractmethod
    def command(self) -> str:
        ...

    async def pre_process(self, runner: 'TaskRunner') -> None:
        pass

    async def post_process(self, runner: 'TaskRunner') -> None:
        pass

    async def on_failure(self, runner: 'TaskRunner') -> None:
        pass
