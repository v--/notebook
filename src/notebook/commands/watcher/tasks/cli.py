import abc
import asyncio
from time import monotonic_ns
from typing import override
lazy import logging
lazy import pathlib
lazy from collections.abc import Iterable

from notebook.paths import AUX_PATH, OUTPUT_PATH, ROOT_PATH

from .base import Task
lazy from .runner import TaskRunner


def format_time(start: int, end: int) -> str:
    delta = end - start
    seconds = delta / 10 ** 9

    if seconds < 10:
        return f'{seconds:02.2f}sec'

    frac_sec = int(seconds) % 60
    frac_min = int(seconds) // 60

    return f'{frac_min:02}:{frac_sec:02}min'


class CliTask(Task):
    bound_logger: logging.LoggerAdapter

    def get_output_path(self, extension: str | None = None) -> pathlib.Path:
        extension = extension if extension is not None else self.get_default_extension()
        return OUTPUT_PATH / self.trigger.path.with_suffix(extension).name

    def get_aux_path(self, extension: str | None = None) -> pathlib.Path:
        extension = extension if extension is not None else self.get_default_extension()
        return AUX_PATH / self.trigger.path.with_suffix(extension).name

    @abc.abstractmethod
    def get_default_extension(self) -> str:
        ...

    @override
    async def clean(self, runner: TaskRunner) -> None:
        start = monotonic_ns()
        self.bound_logger.info(f'Cleanup triggered at {self.created:%H:%M:%S} by {self.reason}')

        for path in self.iter_clean_paths():
            try:
                path.unlink(missing_ok=True)
            except OSError as err:
                self.bound_logger.warning(f'Could not unlink {path}: {err}')

        end = monotonic_ns()
        self.bound_logger.info(f'Cleanup finished in {format_time(start, end)}')

    @override
    async def build(self, runner: TaskRunner) -> None:
        await self.build_pre_process(runner)
        start = monotonic_ns()
        self.bound_logger.info(f'Build triggered by {self.reason}')

        proc = await asyncio.create_subprocess_shell(
            self.get_build_command(),
            stdin=asyncio.subprocess.DEVNULL,
            stdout=self.get_build_out_buffer(),
            stderr=self.get_build_err_buffer(),
            cwd=ROOT_PATH,
        )

        exit_code = await proc.wait()
        end = monotonic_ns()

        if exit_code == 0:
            await self.build_post_process(runner)
            self.bound_logger.info(f'Build finished in {format_time(start, end)}')
        else:
            await self.build_on_failure(runner)
            self.bound_logger.error(f'Build failed with exit code {exit_code} after {format_time(start, end)}')

    @abc.abstractmethod
    def iter_clean_paths(self) -> Iterable[pathlib.Path]:
        pass

    @abc.abstractmethod
    def get_build_command(self) -> str:
        ...

    # ruff: ignore[no-self-use]
    def get_build_out_buffer(self) -> int | None:
        return None

    def get_build_err_buffer(self) -> int | None:
        return self.get_build_out_buffer()

    async def build_pre_process(self, runner: TaskRunner) -> None:
        pass

    async def build_post_process(self, runner: TaskRunner) -> None:
        pass

    async def build_on_failure(self, runner: TaskRunner) -> None:
        pass
