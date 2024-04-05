import asyncio
from datetime import datetime, timedelta
from timeit import default_timer as timer
from typing import ClassVar

from ..common.paths import ROOT_PATH
from .task import WatcherTask


DEBOUNCE_THRESHOLD = timedelta(seconds=1)


class TaskRunner:
    active_aio_tasks: ClassVar[set[asyncio.Task]] = set()
    active_tasks: ClassVar[set[WatcherTask]] = set()
    last_run_attempt: ClassVar[dict[WatcherTask, datetime]] = {}

    async def run_task(self, task: WatcherTask, trigger: str | None = None) -> None:
        self.active_tasks.add(task)
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

        self.active_tasks.remove(task)

    async def run_task_debounced(self, task: WatcherTask, trigger: str | None = None) -> None:
        # This means that the task has already been scheduled
        if task in self.last_run_attempt:
            self.last_run_attempt[task] = datetime.now()
            return

        # Loop asynchronously until enough time has passed since the last scheduling
        while (
            len(self.active_tasks) >= 5 or
            task in self.active_tasks or
            task not in self.last_run_attempt or
            datetime.now() - self.last_run_attempt[task] < DEBOUNCE_THRESHOLD
        ):
            self.last_run_attempt[task] = datetime.now()
            await asyncio.sleep(DEBOUNCE_THRESHOLD.seconds)

        del self.last_run_attempt[task]
        await self.run_task(task, trigger)

    def schedule(self, task: WatcherTask, trigger: str | None = None) -> None:
        aio_task = asyncio.create_task(self.run_task_debounced(task, trigger))
        self.active_aio_tasks.add(aio_task)
        aio_task.add_done_callback(self.active_aio_tasks.discard)
