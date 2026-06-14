import asyncio
import logging
import pathlib
from typing import TYPE_CHECKING

import click
from asyncinotify import Inotify, Mask

from notebook.commands.common.logging import NotebookLoggerHandler
from notebook.paths import FIGURES_PATH, ROOT_PATH

from .tasks import AsymptoteTask, LaTeXCompiler, LaTeXTask, PythonTask, TaskRunner
from .trigger import TaskTrigger, TaskTriggerKind


if TYPE_CHECKING:
    from collections.abc import AsyncIterator


BUILD_MASK = Mask.CLOSE_WRITE | Mask.MOVED_TO
CLEAN_MASK = Mask.MOVED_FROM | Mask.DELETE
MASK = BUILD_MASK | CLEAN_MASK


logger = logging.getLogger(__name__)


async def iter_build_file_changes(inotify: Inotify) -> AsyncIterator[TaskTrigger]:
    inotify.add_watch(ROOT_PATH, MASK)
    inotify.add_watch(ROOT_PATH / 'text', MASK)
    inotify.add_watch(ROOT_PATH / 'packages', MASK)
    inotify.add_watch(ROOT_PATH / 'figures', MASK)
    inotify.add_watch(ROOT_PATH / 'src' / 'notebook' / 'figures', MASK)
    inotify.add_watch(ROOT_PATH / 'images', MASK)
    inotify.add_watch(ROOT_PATH / 'bibliography', MASK)
    inotify.add_watch(ROOT_PATH / 'asymptote', MASK)
    inotify.add_watch(ROOT_PATH / 'classes', MASK)
    inotify.add_watch(ROOT_PATH / 'aux', MASK)
    inotify.add_watch(ROOT_PATH / 'output', MASK)
    logger.info('Started daemon and initialized watchers')

    async for target in inotify:
        if target.path is not None:
            relative = pathlib.Path(target.path).relative_to(ROOT_PATH)

            if target.mask & BUILD_MASK == target.mask:
                yield TaskTrigger(TaskTriggerKind.BUILD, relative)

            if target.mask & CLEAN_MASK == target.mask:
                yield TaskTrigger(TaskTriggerKind.CLEAN, relative)


async def setup_watchers(manager: TaskRunner, inotify: Inotify, rebuild_all_figures: bool) -> None:  # noqa: C901
    async for target in iter_build_file_changes(inotify):
        path = target.path

        if path.match('figures/*.tex'):
            manager.schedule(LaTeXTask(LaTeXCompiler.pdflatex, target, reason='watcher'))

        if path.match('figures/*.asy'):
            manager.schedule(AsymptoteTask(target, reason='watcher'))

        if path.match('src/notebook/figures/*.py') and path.name != '__init__.py':
            manager.schedule(PythonTask(target, reason='watcher'))

        if target.kind == TaskTriggerKind.BUILD or path.match('includeonly'):
            if rebuild_all_figures:
                if path.match('asymptote/*.asy'):
                    for figure_path in FIGURES_PATH.glob('*.asy'):
                        manager.schedule(
                            AsymptoteTask(
                                TaskTrigger(TaskTriggerKind.BUILD, figure_path),
                                reason=path.name,
                            ),
                        )

                if (path.match('classes/*.cls') and not path.match('classes/notebook.cls')) or \
                    path.match('packages/*.sty'):
                    for figure_path in FIGURES_PATH.glob('*.tex'):
                        manager.schedule(
                            LaTeXTask(
                                LaTeXCompiler.pdflatex,
                                TaskTrigger(TaskTriggerKind.BUILD, figure_path),
                                reason=path.name,
                            ),
                        )

            if (
                path.match('notebook.tex') or
                path.match('includeonly') or
                path.match('classes/notebook.cls') or
                path.match('bibliography/*.bib') or
                path.match('text/*.tex') or
                path.match('images/*') or
                path.match('aux/corderef.aux') or
                (path.match('output/*') and not path.match('output/notebook.pdf')) or
                path.match('packages/*.sty')
            ):
                manager.schedule(
                    LaTeXTask(
                        LaTeXCompiler.lualatex,
                        TaskTrigger(TaskTriggerKind.BUILD, ROOT_PATH / 'notebook.tex'),
                        reason=path.name,
                    ),
                )


@click.command()
@click.option('-v', '--verbose', is_flag=True)
@click.option('--rebuild-all-figures', is_flag=True)
def watch(verbose: bool, rebuild_all_figures: bool) -> None:
    base_logger = logging.getLogger('notebook.commands')
    base_logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    base_logger.addHandler(NotebookLoggerHandler(log_subject=True))

    manager = TaskRunner()

    with Inotify() as inotify:
        try:
            asyncio.run(
                setup_watchers(
                    manager,
                    inotify,
                    rebuild_all_figures=rebuild_all_figures,
                ),
            )
        except KeyboardInterrupt:
            manager.finalize()
            logger.info('Gracefully shutting down')
