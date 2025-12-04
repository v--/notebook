import asyncio
import pathlib
from collections.abc import AsyncIterator

import click
import loguru
from asyncinotify import Inotify, Mask
from xvfbwrapper import Xvfb

from ...paths import FIGURES_PATH, ROOT_PATH
from ..common.logging import configure_loguru
from .tasks import AsymptoteTask, LaTeXTask, PythonTask, TaskRunner
from .trigger import TaskTrigger, TaskTriggerKind


BUILD_MASK = Mask.CLOSE_WRITE | Mask.MOVED_TO
CLEAN_MASK = Mask.MOVED_FROM | Mask.DELETE
MASK = BUILD_MASK | CLEAN_MASK


async def iter_build_file_changes(logger: loguru.Logger) -> AsyncIterator[TaskTrigger]:
    with Inotify() as inotify:
        inotify.add_watch(ROOT_PATH, MASK)
        inotify.add_watch(ROOT_PATH / 'text', MASK)
        inotify.add_watch(ROOT_PATH / 'packages', MASK)
        inotify.add_watch(ROOT_PATH / 'figures', MASK)
        inotify.add_watch(ROOT_PATH / 'src' / 'notebook' / 'figures', MASK)
        inotify.add_watch(ROOT_PATH / 'images', MASK)
        inotify.add_watch(ROOT_PATH / 'bibliography', MASK)
        inotify.add_watch(ROOT_PATH / 'asymptote', MASK)
        inotify.add_watch(ROOT_PATH / 'classes', MASK)
        inotify.add_watch(ROOT_PATH / 'output', MASK)
        logger.info('Started daemon and initialized watchers')

        async for target in inotify:
            if target.path is not None:
                relative = pathlib.Path(target.path).relative_to(ROOT_PATH)

                if target.mask & BUILD_MASK == target.mask:
                    yield TaskTrigger(TaskTriggerKind.BUILD, relative)

                if target.mask & CLEAN_MASK == target.mask:
                    yield TaskTrigger(TaskTriggerKind.CLEAN, relative)


async def setup_watchers(manager: TaskRunner, base_logger: loguru.Logger, *, rebuild_all_figures: bool) -> None:
    async for target in iter_build_file_changes(base_logger):
        path = target.path

        if path.match('figures/*.tex'):
            manager.schedule(LaTeXTask(target, reason='watcher', base_logger=base_logger))

        if path.match('figures/*.asy'):
            manager.schedule(AsymptoteTask(target, reason='watcher', base_logger=base_logger))

        if path.match('src/notebook/figures/*.py') and path.name != '__init__.py':
            manager.schedule(PythonTask(target, reason='watcher', base_logger=base_logger))

        if target.kind == TaskTriggerKind.BUILD:
            if rebuild_all_figures:
                if path.match('asymptote/*.asy'):
                    for figure_path in FIGURES_PATH.glob('*.asy'):
                        manager.schedule(
                            LaTeXTask(
                                TaskTrigger(TaskTriggerKind.BUILD, figure_path),
                                reason=path.name,
                                base_logger=base_logger
                            )
                        )

                if (path.match('classes/*.cls') and not path.match('classes/notebook.cls')) or \
                    path.match('packages/*.sty'):
                    for figure_path in FIGURES_PATH.glob('*.tex'):
                        manager.schedule(
                            LaTeXTask(
                                TaskTrigger(TaskTriggerKind.BUILD, figure_path),
                                reason=path.name,
                                base_logger=base_logger
                            )
                        )

            if not path.match('output/notebook.pdf') and (
                path.match('notebook.tex') or
                path.match('includeonly') or
                path.match('classes/notebook.cls') or
                path.match('bibliography/*.bib') or
                path.match('text/*.tex') or
                path.match('images/*') or
                path.match('output/*') or
                path.match('packages/*.sty')
            ):
                manager.schedule(
                    LaTeXTask(
                        TaskTrigger(TaskTriggerKind.BUILD, ROOT_PATH / 'notebook.tex'),
                        reason=path.name,
                        base_logger=base_logger
                    )
                )


@click.command()
@click.option('-v', '--verbose', is_flag=True)
@click.option('--rebuild-all-figures', is_flag=True)
def watch(*, verbose: bool, rebuild_all_figures: bool) -> None:
    configure_loguru(verbose=verbose)
    base_logger = loguru.logger
    manager = TaskRunner()

    vdisplay = Xvfb()
    vdisplay.start()

    try:
        asyncio.run(
            setup_watchers(
                manager,
                base_logger=base_logger,
                rebuild_all_figures=rebuild_all_figures
            )
        )
    except KeyboardInterrupt:
        manager.finalize()
        base_logger.info('Gracefully shutting down')
        vdisplay.stop()
