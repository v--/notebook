import asyncio
import pathlib
from collections.abc import Iterable
from typing import override

from ..trigger import TaskTrigger, TaskTriggerKind
from .cli import CliTask
from .latex import LaTeXTask
from .runner import TaskRunner


class BiberTask(CliTask):
    @override
    def get_default_extension(self) -> str:
        return '.pdf'

    @override
    def iter_clean_paths(self) -> Iterable[pathlib.Path]:
        yield self.get_aux_path('.bbl')  # BibTeX bibliography
        yield self.get_aux_path('.bcf')  # Biber log file
        yield self.get_aux_path('.blg')  # BibTeX log
        yield self.get_aux_path('.run.xml')  # Biber XML file

    @override
    def get_build_command(self) -> str:
        return f'biber {self.bcf_path}'

    @override
    def get_build_out_buffer(self) -> int:
        return asyncio.subprocess.DEVNULL

    @property
    def bcf_path(self) -> pathlib.Path:
        return self.get_aux_path('.bcf')

    @override
    async def build_post_process(self, runner: TaskRunner) -> None:
        runner.schedule(
            LaTeXTask(
                TaskTrigger(TaskTriggerKind.BUILD, self.trigger.path),
                reason=self.bcf_path.as_posix(),
                base_logger=self.base_logger
            )
        )
