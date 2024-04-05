import os.path
import pathlib

import structlog

from ...common.paths import ROOT_PATH
from ..runner import TaskRunner
from ..task import WatcherTask
from .latex import LaTeXTask


class BiberTask(WatcherTask):
    base_logger: structlog.stdlib.BoundLogger
    out_buffer: int | None = None
    biber_path: pathlib.Path
    tex_path: pathlib.Path

    def __init__(self, base_logger: structlog.stdlib.BoundLogger, biber_path: pathlib.Path | str, tex_path: pathlib.Path | str) -> None:
        self.biber_path = pathlib.Path(biber_path)
        self.tex_path = pathlib.Path(tex_path)
        self.base_logger = base_logger
        self.sublogger = base_logger.bind(logger=str(os.path.relpath(self.biber_path, ROOT_PATH)))

    def __repr__(self) -> str:
        return f'BiberTask({self.biber_path!r})'

    @property
    def base_name(self) -> str:
        return self.biber_path.stem

    @property
    def command(self) -> str:
        return f'biber --quiet {self.biber_path}'

    async def post_process(self, runner: TaskRunner) -> None:
        runner.schedule(LaTeXTask(self.base_logger, self.tex_path), str(self.biber_path))
