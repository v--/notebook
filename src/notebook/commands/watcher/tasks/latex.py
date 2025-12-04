import asyncio
import pathlib
import shutil
from collections.abc import Iterable
from typing import override

import texoutparse

from ....paths import AUX_PATH
from ..trigger import TaskTrigger, TaskTriggerKind
from .cli import CliTask
from .runner import TaskRunner


TEX_LOG_ENCODING = 'latin-1'


class LaTeXTask(CliTask):
    @override
    def get_default_extension(self) -> str:
        return '.pdf'

    @override
    def iter_clean_paths(self) -> Iterable[pathlib.Path]:
        yield self.get_aux_path('.aux')  # Principal auxiliary file
        yield self.get_aux_path('.log')  # Principal log file
        yield self.get_aux_path('.old.log')  # Copy of old build log (that can be viewed while the new one is being generated)
        yield self.get_aux_path('.blg')  # Outline data
        yield self.get_aux_path('.toc')  # Table of contents data
        yield self.get_aux_path('.pdf')
        yield self.get_output_path('.pdf')

    @override
    def get_build_command(self) -> str:
        return r'pdflatex -interaction=batchmode -output-directory=%s %s' % (AUX_PATH, self.trigger.path)

    @override
    def get_build_out_buffer(self) -> int:
        return asyncio.subprocess.DEVNULL

    @override
    async def build_post_process(self, runner: TaskRunner) -> None:
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
            runner.schedule(
                LaTeXTask(
                    TaskTrigger(TaskTriggerKind.BUILD, self.trigger.path),
                    reason='rerunfilecheck',
                    base_logger=self.base_logger
                )
            )
        elif requires_biber_rerun:
            from .biber import BiberTask  # Avoid circular import  # noqa: PLC0415
            runner.schedule(
                BiberTask(
                    TaskTrigger(TaskTriggerKind.BUILD, self.trigger.path),
                    reason=self.trigger.path.name,
                    base_logger=self.base_logger
                )
            )
        else:
            output_path = self.get_output_path()
            self.sublogger.debug('No more passes required.')
            shutil.copyfile(self.get_aux_path('.pdf'), output_path)

    build_on_failure = build_post_process
