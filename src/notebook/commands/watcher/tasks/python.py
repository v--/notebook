import pathlib
import shutil
from collections.abc import Iterable
from typing import override

from .cli import CliTask
from .runner import TaskRunner


class PythonTask(CliTask):
    @override
    def get_default_extension(self) -> str:
        return '.pdf'

    @override
    def iter_clean_paths(self) -> Iterable[pathlib.Path]:
        yield self.get_aux_path()
        yield self.get_output_path()

    @override
    def get_build_command(self) -> str:
        return f'python -m src.notebook.figures.{self.trigger.path.stem}'

    @override
    async def build_post_process(self, runner: TaskRunner) -> None:
        aux_path = self.get_aux_path()
        output_path = self.get_output_path()

        if not aux_path.exists():
            self.sublogger.error('No output file')
            return

        shutil.copyfile(aux_path, output_path)
