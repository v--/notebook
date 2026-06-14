import asyncio
import logging
from typing import TYPE_CHECKING, override

from notebook.commands.watcher.trigger import TaskTrigger, TaskTriggerKind

from .cli import CliTask
from .latex import LaTeXCompiler, LaTeXTask


if TYPE_CHECKING:
    import pathlib
    from collections.abc import Iterable

    from .runner import TaskRunner


logger = logging.getLogger(__name__)


class BiberTask(CliTask):
    def __init__(self, trigger: TaskTrigger, reason: str) -> None:
        super().__init__(trigger, reason)
        self.logger = logging.LoggerAdapter(logger, extra={'subject': self.trigger.path.name})

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
                LaTeXCompiler.lualatex,
                TaskTrigger(TaskTriggerKind.BUILD, self.trigger.path),
                reason=self.bcf_path.as_posix(),
            ),
        )
