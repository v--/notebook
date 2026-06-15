import logging
import shutil
from typing import TYPE_CHECKING, override

from .cli import CliTask


if TYPE_CHECKING:
    import pathlib
    from collections.abc import Iterable

    from notebook.commands.watcher.trigger import TaskTrigger

    from .runner import TaskRunner


logger = logging.getLogger(__name__)


class AsymptoteTask(CliTask):
    def __init__(self, trigger: TaskTrigger, reason: str) -> None:
        super().__init__(trigger, reason)
        self.bound_logger = logging.LoggerAdapter(logger, extra={'subject': self.trigger.path.name})

    @override
    def get_default_extension(self) -> str:
        return '.pdf'

    @override
    def iter_clean_paths(self) -> Iterable[pathlib.Path]:
        yield self.get_aux_path()
        yield self.get_output_path()

    @override
    def get_build_command(self) -> str:
        return f'asy -outname={self.get_aux_path().with_suffix('')} {self.trigger.path}'

    @override
    async def build_pre_process(self, runner: TaskRunner) -> None:
        self.get_aux_path().unlink(missing_ok=True)

    @override
    async def build_post_process(self, runner: TaskRunner) -> None:
        aux_path = self.get_aux_path()
        output_path = self.get_output_path()

        if not aux_path.exists():
            self.bound_logger.error('No output file')
            return

        shutil.copyfile(aux_path, output_path)
