import asyncio
import os.path
import pathlib
import shutil

import structlog
import texoutparse

from ...common.paths import AUX_PATH, OUTPUT_PATH, ROOT_PATH
from ..runner import TaskRunner
from ..task import WatcherTask


TEX_LOG_ENCODING = 'latin-1'


class LaTeXTask(WatcherTask):
    tex_path: pathlib.Path
    out_buffer: int | None = asyncio.subprocess.DEVNULL
    _bcf_file_hash: int | None = None

    def __init__(self, base_logger: structlog.stdlib.BoundLogger, tex_path: pathlib.Path | str) -> None:
        self.tex_path = pathlib.Path(tex_path)
        self.base_logger = base_logger
        self.sublogger = base_logger.bind(logger=str(os.path.relpath(self.tex_path, ROOT_PATH)))

    def __repr__(self) -> str:
        return f'LaTeXTask({self.tex_path!r})'

    def get_aux_path(self, extension: str) -> pathlib.Path:
        return AUX_PATH / self.tex_path.with_suffix(extension).name

    @property
    def build_pdf_path(self) -> pathlib.Path:
        return OUTPUT_PATH / self.tex_path.with_suffix('.pdf').name

    @property
    def command(self) -> str:
        return r'pdflatex -interaction=batchmode -output-directory=%s %s' % (AUX_PATH, self.tex_path)  # noqa: UP031

    def get_bcf_hash(self) -> int | None:
        try:
            with self.get_aux_path('.bcf').open() as bcf_file:
                return hash(bcf_file.read())
        except OSError:
            return None

    async def pre_process(self, runner: TaskRunner) -> None:  # noqa: ARG002
        self._bcf_file_hash = self.get_bcf_hash()

    async def post_process(self, runner: TaskRunner) -> None:  # noqa: PLR0912
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
            from .biber import BiberTask  # Avoid circular import
            runner.schedule(BiberTask(self.base_logger, self.get_aux_path('.bcf'), self.tex_path), str(self.tex_path))

        if requires_rerun:
            runner.schedule(self, 'last build')
        else:
            self.sublogger.debug(f'No more passes required. Copying {self.get_aux_path(".pdf")} to {self.build_pdf_path}')
            shutil.copyfile(self.get_aux_path('.pdf'), self.build_pdf_path)

    on_failure = post_process
