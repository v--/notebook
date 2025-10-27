import asyncio
import os.path
import pathlib
from typing import override

import loguru

from ....paths import AUX_PATH, OUTPUT_PATH, ROOT_PATH
from ..runner import TaskRunner
from ..task import WatcherTask
from .latex import LaTeXTask


class BiberTask(WatcherTask):
    base_logger: 'loguru.Logger'
    out_buffer: int | None = asyncio.subprocess.DEVNULL
    tex_path: pathlib.Path

    def __init__(self, base_logger: 'loguru.Logger', tex_path: pathlib.Path | str) -> None:
        self.tex_path = pathlib.Path(tex_path)
        self.base_logger = base_logger
        self.sublogger = base_logger.bind(logger=str(os.path.relpath(self.bcf_path, ROOT_PATH)))

    def __repr__(self) -> str:
        return f'BiberTask({self.bcf_path!r})'

    @override
    @property
    def command(self) -> str:
        return f'biber {self.bcf_path}'

    @property
    def build_pdf_path(self) -> pathlib.Path:
        return OUTPUT_PATH / self.tex_path.with_suffix('.pdf').name

    def get_aux_path(self, extension: str) -> pathlib.Path:
        return AUX_PATH / self.tex_path.with_suffix(extension).name

    @property
    def bcf_path(self) -> pathlib.Path:
        return self.get_aux_path('.bcf')

    @override
    async def post_process(self, runner: TaskRunner) -> None:
        runner.schedule(LaTeXTask(self.base_logger, self.tex_path), str(self.bcf_path))
