import asyncio
import os.path
import pathlib
import shutil
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from enum import Enum
from fnmatch import fnmatch
from timeit import default_timer as timer
from typing import AsyncIterator, ClassVar

import structlog
import texoutparse
from asyncinotify import Inotify, Mask


DEBOUNCE_THRESHOLD = timedelta(seconds=1)
TEX_LOG_ENCODING = 'latin-1'

ROOT_DIR = pathlib.Path().resolve()

while not (ROOT_DIR / 'notebook.tex').exists():
    ROOT_DIR = ROOT_DIR.parent

AUX_DIR = ROOT_DIR / 'aux'
OUTPUT_DIR = ROOT_DIR / 'output'
FIGURES_DIR = ROOT_DIR / 'figures'


class WatchTarget(Enum):
    all = 'all'
    notebook = 'notebook'
    figures = 'figures'


class Task(ABC):
    sublogger: structlog.stdlib.BoundLogger
    out_buffer: int | None

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Task) and self.command == other.command

    def __hash__(self) -> int:
        return hash(self.command)

    @property
    @abstractmethod
    def command(self) -> str:
        pass

    async def pre_process(self, runner: 'TaskRunner') -> None:  # noqa: B027
        pass

    async def post_process(self, runner: 'TaskRunner') -> None:  # noqa: B027
        pass

    async def on_failure(self, runner: 'TaskRunner') -> None:  # noqa: B027
        pass


class BiberTask(Task):
    base_logger: structlog.stdlib.BoundLogger
    out_buffer: int | None = None
    biber_path: pathlib.Path
    tex_path: pathlib.Path

    def __init__(self, base_logger: structlog.stdlib.BoundLogger, biber_path: pathlib.Path | str, tex_path: pathlib.Path | str) -> None:
        self.biber_path = pathlib.Path(biber_path)
        self.tex_path = pathlib.Path(tex_path)
        self.base_logger = base_logger
        self.sublogger = base_logger.bind(logger=str(os.path.relpath(self.biber_path, ROOT_DIR)))

    def __repr__(self) -> str:
        return f'BiberTask({self.biber_path!r})'

    @property
    def base_name(self) -> str:
        return self.biber_path.stem

    @property
    def command(self) -> str:
        return f'biber --quiet {self.biber_path}'

    async def post_process(self, runner: 'TaskRunner') -> None:
        runner.schedule(TeXTask(self.base_logger, self.tex_path), str(self.biber_path))


class TeXTask(Task):
    tex_path: pathlib.Path
    out_buffer: int | None = asyncio.subprocess.DEVNULL
    _bcf_file_hash: int | None = None

    def __init__(self, base_logger: structlog.stdlib.BoundLogger, tex_path: pathlib.Path | str) -> None:
        self.tex_path = pathlib.Path(tex_path)
        self.base_logger = base_logger
        self.sublogger = base_logger.bind(logger=str(os.path.relpath(self.tex_path, ROOT_DIR)))

    def __repr__(self) -> str:
        return f'TeXTask({self.tex_path!r})'

    def get_aux_path(self, extension: str) -> pathlib.Path:
        return AUX_DIR / self.tex_path.with_suffix(extension).name

    @property
    def build_pdf_path(self) -> pathlib.Path:
        return OUTPUT_DIR / self.tex_path.with_suffix('.pdf').name

    @property
    def command(self) -> str:
        return r'pdflatex -interaction=batchmode -output-directory=%s %s' % (AUX_DIR, self.tex_path)  # noqa: UP031

    def get_bcf_hash(self) -> int | None:
        try:
            with self.get_aux_path('.bcf').open() as bcf_file:
                return hash(bcf_file.read())
        except OSError:
            return None

    async def pre_process(self, runner: 'TaskRunner') -> None:  # noqa: ARG002
        self._bcf_file_hash = self.get_bcf_hash()

    async def post_process(self, runner: 'TaskRunner') -> None:  # noqa: PLR0912
        parser = texoutparse.LatexLogParser()
        requires_rerun = False

        try:
            with self.get_aux_path('.log').open(encoding=TEX_LOG_ENCODING) as log_file:
                requires_rerun = 'Rerun to get' in log_file.read()
                log_file.seek(0)
                parser.process(log_file)
        except OSError:
            self.sublogger.exception('Could not open TeX log file.')
        else:
            if len(parser.errors) > 0:
                if len(parser.errors) == 1:
                    self.sublogger.error(f'Compiled with an error:\n {parser.errors[0]!s}')
                else:
                    self.sublogger.error(f'Compiled with {len(parser.errors)} errors. The first error is:\n {parser.errors[0]!s}')
            elif len(parser.warnings) > 0:
                if len(parser.warnings) == 1:
                    self.sublogger.warning(f'Compiled with a warning:\n {parser.warnings[0]!s}')
                else:
                    self.sublogger.warning(f'Compiled with {len(parser.warnings)} warnings. The first warning is:\n {parser.warnings[0]!s}')
            elif len(parser.badboxes) > 0:
                if len(parser.badboxes) == 1:
                    self.sublogger.warning(f'Compiled with a bad box:\n {parser.badboxes[0]!s}')
                else:
                    self.sublogger.warning(f'Compiled with {len(parser.badboxes)} bad boxes. The first bad box is:\n {parser.badboxes[0]!s}')

        if len(parser.errors) != 0:
            return

        if not self.get_aux_path('.pdf').exists():
            self.sublogger.error('No output file')
            return

        if self.get_bcf_hash() != self._bcf_file_hash:
            runner.schedule(BiberTask(self.base_logger, self.get_aux_path('.bcf'), self.tex_path), str(self.tex_path))

        if requires_rerun:
            runner.schedule(self, 'last build')
        else:
            self.sublogger.debug(f'No more passes required. Copying {self.get_aux_path(".pdf")} to {self.build_pdf_path}')
            shutil.copyfile(self.get_aux_path('.pdf'), self.build_pdf_path)

    on_failure = post_process


class AsymptoteTask(Task):
    src_path: pathlib.Path
    out_buffer: int | None = None

    def __init__(self, base_logger: structlog.stdlib.BoundLogger, src_path: pathlib.Path | str) -> None:
        self.src_path = pathlib.Path(src_path)
        self.base_logger = base_logger
        self.sublogger = base_logger.bind(logger=str(self.src_path))

    def __repr__(self) -> str:
        return f'AsymptoteTask({self.src_path!r})'

    @property
    def aux_eps_path(self) -> pathlib.Path:
        return AUX_DIR / self.src_path.with_suffix('.eps').name

    @property
    def build_eps_path(self) -> pathlib.Path:
        return OUTPUT_DIR / self.src_path.with_suffix('.eps').name

    @property
    def command(self) -> str:
        return f'asy -quiet -render=0 -outlogger={self.aux_eps_path} {self.src_path}'

    async def post_process(self, runner: 'TaskRunner') -> None:  # noqa: ARG002
        shutil.copyfile(self.aux_eps_path, self.build_eps_path)


class TaskRunner:
    active_aio_tasks: ClassVar[set[asyncio.Task]] = set()
    active_tasks: ClassVar[set[Task]] = set()
    last_run_attempt: ClassVar[dict[Task, datetime]] = {}

    async def run_task(self, task: Task, trigger: str | None = None) -> None:
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
            cwd=ROOT_DIR
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

    async def run_task_debounced(self, task: Task, trigger: str | None = None) -> None:
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

    def schedule(self, task: Task, trigger: str | None = None) -> None:
        aio_task = asyncio.create_task(self.run_task_debounced(task, trigger))
        self.active_aio_tasks.add(aio_task)
        aio_task.add_done_callback(self.active_aio_tasks.discard)


async def iter_file_changes(logger: structlog.stdlib.BoundLogger) -> AsyncIterator:
    with Inotify() as inotify:
        inotify.add_watch(ROOT_DIR, Mask.MODIFY)
        inotify.add_watch(ROOT_DIR / 'text', Mask.MODIFY)
        inotify.add_watch(ROOT_DIR / 'packages', Mask.MODIFY)
        inotify.add_watch(ROOT_DIR / 'figures', Mask.MODIFY)
        inotify.add_watch(ROOT_DIR / 'bibliography', Mask.MODIFY)
        inotify.add_watch(ROOT_DIR / 'asymptote', Mask.MODIFY)
        inotify.add_watch(ROOT_DIR / 'classes', Mask.MODIFY)
        inotify.add_watch(ROOT_DIR / 'output', Mask.MODIFY)
        logger.info('Started daemon and initialized watchers')

        async for event in inotify:
            if event.path is not None:
                yield os.path.relpath(event.path, ROOT_DIR)


async def setup_watchers(target: WatchTarget, base_logger: structlog.stdlib.BoundLogger) -> None:
    runner = TaskRunner()

    async for path in iter_file_changes(base_logger):
        if target in [WatchTarget.all, WatchTarget.figures]:
            if fnmatch(path, 'classes/tikzcd.cls') or fnmatch(path, 'classes/forest.cls') or fnmatch(path, 'packages/*.sty'):
                for figure_path in FIGURES_DIR.glob('*.tex'):
                    runner.schedule(TeXTask(base_logger, figure_path), trigger=str(path))

            if fnmatch(path, 'figures/*.tex'):
                runner.schedule(TeXTask(base_logger, path), trigger=str(path))

            if fnmatch(path, 'figures/*.asy'):
                runner.schedule(AsymptoteTask(base_logger, path), trigger=str(path))

            if fnmatch(path, 'asymptote/*.asy'):
                for figure_path in FIGURES_DIR.glob('*.asy'):
                    runner.schedule(AsymptoteTask(base_logger, figure_path), trigger=str(path))

        if target in [WatchTarget.all, WatchTarget.notebook] and \
            not fnmatch(path, 'output/notebook.pdf') and (
                fnmatch(path, 'notebook.tex') or
                fnmatch(path, 'classes/notebook.cls') or
                fnmatch(path, 'bibliography/*.bib') or
                fnmatch(path, 'text/*.tex') or
                fnmatch(path, 'output/*.pdf') or
                fnmatch(path, 'packages/*.sty')
        ):
            runner.schedule(TeXTask(base_logger, ROOT_DIR / 'notebook.tex'), trigger=str(path))


if __name__ == '__main__':
    import sys

    try:
        target = WatchTarget[sys.argv[1]]
    except IndexError:
        print('What to watch?', file=sys.stderr)  # noqa: T201
    except KeyError:
        print(f'Invalid target {sys.argv[1]}. Expected {" or ".join(repr(t.value) for t in WatchTarget)}.', file=sys.stderr)  # noqa: T201
    else:
        base_logger = structlog.get_logger().bind(logger='<system>')

        try:
            asyncio.run(setup_watchers(target, base_logger))
        except KeyboardInterrupt:
            base_logger.info('Gracefully shutting down')
