import asyncio
import functools
from collections import deque
from dataclasses import dataclass
from datetime import datetime
from timeit import default_timer as timer
from typing import ClassVar

from ...paths import ROOT_PATH
from .task import WatcherTask


@dataclass
class TimedTask:
    task: WatcherTask
    queued_at: datetime
    trigger: str | None


class TaskRunner:
    running_tasks: ClassVar[set[WatcherTask]]= set()
    running_aio_tasks: ClassVar[set[asyncio.Task]]= set()
    queued_tasks: ClassVar[deque[TimedTask]] = deque()

    async def run_task(self, task: WatcherTask, trigger: str | None = None) -> None:
        await task.pre_process(self)
        start = timer()

        if trigger is None:
            task.sublogger.info('Manually triggered')
        else:
            task.sublogger.info(f'Triggered by {trigger}')

        proc = await asyncio.create_subprocess_shell(
            task.command,
            stdin=asyncio.subprocess.DEVNULL,
            stdout=task.out_buffer,
            stderr=task.out_buffer,
            cwd=ROOT_PATH
        )

        exit_code = await proc.wait()

        if exit_code == 0:
            await task.post_process(self)
            ms = round(1000 * (timer() - start))
            task.sublogger.info(f'Finished in {ms}ms')
        else:
            await task.on_failure(self)
            ms = round(1000 * (timer() - start))
            task.sublogger.error(f'Failed in {ms}ms with exit code {exit_code}')

    def run_queued(self) -> None:
        for timed_task in list(self.queued_tasks):
            if timed_task.task not in self.running_tasks:
                self.queued_tasks.remove(timed_task)
                self.schedule(timed_task.task, timed_task.trigger)

    def ensure_in_queue(self, task: WatcherTask, trigger: str | None = None) -> None:
        now = datetime.now()

        for timed_task in list(self.queued_tasks):
            if timed_task.task == task:
                timed_task.queued_at = now
                timed_task.trigger = trigger
                break
        else:
            self.queued_tasks.append(TimedTask(task, now, trigger))

    def on_finish(self, task: WatcherTask, aio_task: asyncio.Task) -> None:
        self.running_aio_tasks.discard(aio_task)
        self.running_tasks.discard(task)
        self.run_queued()

    def schedule(self, task: WatcherTask, trigger: str | None = None) -> None:
        if task in self.running_tasks:
            self.ensure_in_queue(task, trigger)
            return

        self.running_tasks.add(task)
        aio_task = asyncio.create_task(self.run_task(task, trigger))
        self.running_aio_tasks.add(aio_task)
        aio_task.add_done_callback(functools.partial(self.on_finish, task))
