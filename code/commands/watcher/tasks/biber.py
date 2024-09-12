import asyncio
import os.path
import pathlib
import shutil

import loguru

from ...common.paths import AUX_PATH, OUTPUT_PATH, ROOT_PATH
from ..runner import TaskRunner
from ..task import WatcherTask
from .latex import LaTeXTask


class BiberTask(WatcherTask):
    base_logger: 'loguru.Logger'
    out_buffer: int | None = asyncio.subprocess.DEVNULL
    tex_path: pathlib.Path
    _bbl_hash: int | None

    def __init__(self, base_logger: 'loguru.Logger', tex_path: pathlib.Path | str) -> None:
        self.tex_path = pathlib.Path(tex_path)
        self.base_logger = base_logger
        self.sublogger = base_logger.bind(logger=str(os.path.relpath(self.bcf_path, ROOT_PATH)))
        self._bbl_hash = None

    def __repr__(self) -> str:
        return f'BiberTask({self.bcf_path!r})'

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

    def get_bbl_hash(self) -> int | None:
        try:
            with self.get_aux_path('.bbl').open() as bbl_file:
                return hash(bbl_file.read())
        except OSError:
            return None

    async def pre_process(self, runner: TaskRunner) -> None:  # noqa: ARG002
        self._bcf_file_hash = self.get_bbl_hash()

    async def post_process(self, runner: TaskRunner) -> None:
        if self._bcf_file_hash == self.get_bbl_hash():
            self.sublogger.info(f'Ignoring futile biber run and copying {self.get_aux_path(".pdf")} to {self.build_pdf_path}')
            shutil.copyfile(self.get_aux_path('.pdf'), self.build_pdf_path)
            return

        runner.schedule(LaTeXTask(self.base_logger, self.tex_path), str(self.bcf_path))
