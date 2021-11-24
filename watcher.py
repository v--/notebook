from datetime import datetime, timedelta
from fnmatch import fnmatch
from timeit import default_timer as timer
from typing import Optional
import asyncio
import os.path
import pathlib

from asyncinotify import Inotify, Mask
from loguru import logger
import texoutparse


DEBOUNCE_THRESHOLD = timedelta(seconds=1)
TEX_LOG_ENCODING = 'latin-1'


class Task:
    modified_file: str
    command: str
    out_buffer: int

    def __init__(self):
        self.sublogger = logger.bind(name=self.command)

    def __eq__(self, other):
        return isinstance(other, Task) and self.command == other.command

    def __hash__(self):
        return hash(self.command)

    async def pre_process(self):
        return []

    async def post_process(self):
        return []


class BiberTask(Task):
    modified_file: str
    out_buffer: int = asyncio.subprocess.PIPE

    def __init__(self, modified_file: str):
        self.modified_file = modified_file
        super().__init__()

    def __repr__(self):
        return f'BiberTask({repr(self.modified_file)})'

    @property
    def command(self):
        return f'biber {self.modified_file}'


class TeXTask(Task):
    tex_file: str
    out_buffer: int = asyncio.subprocess.DEVNULL
    _bcf_file_hash: Optional[int] = None

    def __init__(self, modified_file: str, tex_file: str):
        self.modified_file = modified_file
        self.tex_file = tex_file
        super().__init__()

    def __repr__(self):
        return f'TeXTask({repr(self.base_name)})'

    @property
    def base_name(self):
        return os.path.splitext(self.tex_file)[0]

    @property
    def pdf_file(self):
        return self.base_name + '.pdf'

    @property
    def log_file(self):
        return self.base_name + '.log'

    @property
    def bcf_file(self):
        return self.base_name + '.bcf'

    @property
    def command(self):
        return f'make {self.pdf_file}'

    def get_bcf_hash(self) -> Optional[int]:
        try:
            with open(self.bcf_file, 'r') as bcf_file:
                return hash(bcf_file.read())
        except IOError:
            return None

    async def pre_process(self):
        self._bcf_file_hash = self.get_bcf_hash()
        return []

    async def post_process(self):
        parser = texoutparse.LatexLogParser()

        try:
            with open(self.log_file, 'r', encoding=TEX_LOG_ENCODING) as log_file:
                parser.process(log_file)
        except OSError:
            self.sublogger.error('Could not open TeX log file.')
        else:
            if len(parser.errors) > 0:
                self.sublogger.error(f'Compiled with {len(parser.errors)} errors. The first error is:\n {str(parser.errors[0])}')
            elif len(parser.warnings) > 0:
                self.sublogger.warning(f'Compiled with {len(parser.warnings)} warnings. The first warning is:\n {str(parser.warnings[0])}')
            elif len(parser.badboxes) > 0:
                self.sublogger.warning(f'Compiled with {len(parser.badboxes)} bad boxes. The first bad box is:\n {str(parser.badboxes[0])}')
            else:
                self.sublogger.info('Compiled without warnings.')

        if self.get_bcf_hash() != self._bcf_file_hash:
            return [BiberTask(self.bcf_file)]

        return []


class MakeTask(Task):
    make_task: str
    out_buffer: int = asyncio.subprocess.PIPE

    def __init__(self, modified_file: str, make_task: str):
        self.modified_file = modified_file
        self.make_task = make_task
        super().__init__()

    def __repr__(self):
        return f'MakeTask({repr(self.make_task)})'

    @property
    def command(self):
        return f'make {self.make_task}'


class TaskRunner:
    active_tasks: set[Task] = set()
    last_run_attempt: dict[Task, datetime] = {}

    async def run_task(self, task: Task):
        task.sublogger.info(f'Running because {task.modified_file} was modified.')
        self.active_tasks.add(task)

        start = timer()

        for new_task in await task.pre_process():
            await self.run_task(new_task)

        proc = await asyncio.create_subprocess_shell(
            task.command,
            stdout=task.out_buffer,
            stderr=task.out_buffer,
        )

        await proc.communicate()

        for new_task in await task.post_process():
            await self.run_task(new_task)

        self.active_tasks.remove(task)

        ms = round(1000 * (timer() - start))
        task.sublogger.info(f'Finished in {ms}ms.')

    async def run_task_debounced(self, task: Task):
        # This means that the task has already been scheduled
        if task in self.last_run_attempt:
            self.last_run_attempt[task] = datetime.now()
            return

        # Loop asynchronously until enough time has passed since the last scheduling
        while task in self.active_tasks or task not in self.last_run_attempt or datetime.now() - self.last_run_attempt[task] < DEBOUNCE_THRESHOLD:
            self.last_run_attempt[task] = datetime.now()
            await asyncio.sleep(DEBOUNCE_THRESHOLD.seconds)

        del self.last_run_attempt[task]
        await self.run_task(task)

    def schedule(self, task: Task):
        asyncio.create_task(self.run_task_debounced(task))


async def iter_file_changes():
    root = pathlib.Path('.')
    sublogger = logger.bind(name='<system>')

    with Inotify() as inotify:
        inotify.add_watch(root, Mask.MODIFY)
        inotify.add_watch(root / 'src', Mask.MODIFY)
        inotify.add_watch(root / 'figures', Mask.MODIFY)
        inotify.add_watch(root / 'packages', Mask.MODIFY)
        sublogger.info('Started daemon and initialized watchers')

        async for event in inotify:
            if event.path is not None:
                yield event.path


async def setup_watchers():
    runner = TaskRunner()

    async for path in iter_file_changes():
        if path == 'tikzcd.cls':
            runner.schedule(MakeTask(path, 'figures'))

        if fnmatch(path, 'figures/*[!_].tex'):
            runner.schedule(TeXTask(path, path))

        if fnmatch(path, 'figures/*.asy'):
            runner.schedule(MakeTask(path, os.path.splitext(path)[0] + '.pdf'))

        if fnmatch(path, 'figures/*.pdf'):
            runner.schedule(TeXTask(path, 'notebook.tex'))

        if fnmatch(path, 'packages/*.sty'):
            runner.schedule(MakeTask(path, 'figures'))
            runner.schedule(TeXTask(path, 'notebook.tex'))

        if fnmatch(path, 'src/*.tex') or path == 'notebook.cls':
            runner.schedule(TeXTask(path, 'notebook.tex'))


if __name__ == '__main__':
    import sys
    logger.remove()
    logger.add(sys.stdout, colorize=True, format='<green>{time:HH:mm:ss}</green> | <level>{level:7}</level> | {extra[name]} | <level>{message}</level>')
    asyncio.run(setup_watchers())
