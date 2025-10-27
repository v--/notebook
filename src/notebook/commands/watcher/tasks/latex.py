import asyncio
import os.path
import pathlib
import shutil
from typing import override

import loguru
import texoutparse

from ....paths import AUX_PATH, OUTPUT_PATH, ROOT_PATH
from ..runner import TaskRunner
from ..task import WatcherTask


TEX_LOG_ENCODING = 'latin-1'


class LaTeXTask(WatcherTask):
    tex_path: pathlib.Path
    out_buffer: int | None = asyncio.subprocess.DEVNULL

    def __init__(self, base_logger: loguru.Logger, tex_path: pathlib.Path | str) -> None:
        self.tex_path = pathlib.Path(tex_path)
        self.base_logger = base_logger
        self.sublogger = base_logger.bind(logger=str(os.path.relpath(self.tex_path, ROOT_PATH)))

    def __repr__(self) -> str:
        return f'LaTeXTask({self.tex_path!r})'

    @property
    def build_pdf_path(self) -> pathlib.Path:
        return OUTPUT_PATH / self.tex_path.with_suffix('.pdf').name

    @property
    @override
    def command(self) -> str:
        return r'pdflatex -interaction=batchmode -output-directory=%s %s' % (AUX_PATH, self.tex_path)

    def get_aux_path(self, extension: str) -> pathlib.Path:
        return AUX_PATH / self.tex_path.with_suffix(extension).name

    @override
    async def post_process(self, runner: TaskRunner) -> None:
        parser = texoutparse.LatexLogParser()
        requires_rerun = False
        requires_biber_rerun = False

        try:
            with self.get_aux_path('.log').open(encoding=TEX_LOG_ENCODING) as log_file:
                shutil.copyfile(self.get_aux_path('.log'), self.get_aux_path('.old.log'))
                requires_rerun = 'Rerun to get' in log_file.read()
                log_file.seek(0)
                requires_biber_rerun = 'Please (re)run Biber' in log_file.read()
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

        if requires_rerun:
            runner.schedule(LaTeXTask(self.base_logger, self.tex_path), 'rerunfilecheck')
        elif requires_biber_rerun:
            from .biber import BiberTask  # Avoid circular import  # noqa: PLC0415
            runner.schedule(BiberTask(self.base_logger, self.tex_path), str(self.tex_path))
        else:
            self.sublogger.debug(f'No more passes required. Copying {self.get_aux_path(".pdf")} to {self.build_pdf_path}')
            shutil.copyfile(self.get_aux_path('.pdf'), self.build_pdf_path)

    on_failure = post_process
