import asyncio
from dataclasses import dataclass

from ..trigger import TaskTrigger, TaskTriggerKind
from .base import Task


@dataclass
class TaskRunnerItem:
    task: Task
    aio_task: asyncio.Task | None = None
    next_task: Task | None = None


class TaskRunner:
    _max_simultaneous: int
    _queue: dict[TaskTrigger, TaskRunnerItem]

    def __init__(self, max_simultaneous: int = 4) -> None:
        self._max_simultaneous = max_simultaneous
        self._queue = {}

    async def _run_task(self, item: TaskRunnerItem) -> None:
        match item.task.trigger.kind:
            case TaskTriggerKind.CLEAN:
                await item.task.clean(self)

            case TaskTriggerKind.BUILD:
                await item.task.build(self)

        if item.next_task:
            del item.aio_task
            item.task = item.next_task
            del item.next_task
        else:
            del self._queue[item.task.trigger]

        self.run_queued()

    def _find_earliest_unran(self) -> TaskRunnerItem | None:
        return min(
            (item for item in self._queue.values() if item.aio_task is None),
            key=lambda item: item.task.created.timestamp(),
            default=None
        )

    def _get_running_count(self) -> int:
        return sum(1 for item in self._queue.values() if item.aio_task)

    def run_queued(self) -> None:
        if self._get_running_count() == self._max_simultaneous:
            return

        if item := self._find_earliest_unran():
            item.aio_task = asyncio.Task(self._run_task(item))
            self.run_queued()

    def schedule(self, task: Task) -> None:
        existing = self._queue.get(task.trigger)

        if existing:
            if existing.aio_task is None:
                existing.task = task
            else:
                existing.next_task = task
        else:
            self._queue[task.trigger] = TaskRunnerItem(task)
            self.run_queued()

    def finalize(self) -> None:
        for item in self._queue.values():
            if item.aio_task:
                item.aio_task.cancel()
                del self._queue[item.task.trigger]
