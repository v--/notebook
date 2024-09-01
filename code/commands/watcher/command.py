import asyncio
import os.path
from collections.abc import AsyncIterator
from fnmatch import fnmatch
from typing import Literal

import click
import structlog
from asyncinotify import Inotify, Mask

from ..common.paths import FIGURES_PATH, ROOT_PATH
from .runner import TaskRunner
from .tasks import AsymptoteTask, LaTeXTask


WatchTarget = Literal['all', 'notebook', 'figures']


async def iter_file_changes(logger: structlog.stdlib.BoundLogger) -> AsyncIterator:
    with Inotify() as inotify:
        inotify.add_watch(ROOT_PATH, Mask.MODIFY)
        inotify.add_watch(ROOT_PATH / 'text', Mask.MODIFY)
        inotify.add_watch(ROOT_PATH / 'packages', Mask.MODIFY)
        inotify.add_watch(ROOT_PATH / 'figures', Mask.MODIFY)
        inotify.add_watch(ROOT_PATH / 'images', Mask.MODIFY)
        inotify.add_watch(ROOT_PATH / 'bibliography', Mask.MODIFY)
        inotify.add_watch(ROOT_PATH / 'asymptote', Mask.MODIFY)
        inotify.add_watch(ROOT_PATH / 'classes', Mask.MODIFY)
        inotify.add_watch(ROOT_PATH / 'output', Mask.MODIFY)
        logger.info('Started daemon and initialized watchers')

        async for event in inotify:
            if event.path is not None:
                yield os.path.relpath(event.path, ROOT_PATH)


async def setup_watchers(base_logger: structlog.stdlib.BoundLogger, *, no_aux: bool) -> None:
    runner = TaskRunner()

    async for path in iter_file_changes(base_logger):
        if no_aux and (fnmatch(path, '*.cls') or fnmatch(path, '*.sty')):
            continue

        if (fnmatch(path, 'classes/*.cls') and not fnmatch(path, 'classes/notebook.cls')) or \
            fnmatch(path, 'packages/*.sty'):
            for figure_path in FIGURES_PATH.glob('*.tex'):
                runner.schedule(LaTeXTask(base_logger, figure_path), trigger=str(path))

        if fnmatch(path, 'figures/*.tex'):
            runner.schedule(LaTeXTask(base_logger, path), trigger=str(path))

        if fnmatch(path, 'figures/*.asy'):
            runner.schedule(AsymptoteTask(base_logger, path), trigger=str(path))

        if fnmatch(path, 'asymptote/*.asy'):
            for figure_path in FIGURES_PATH.glob('*.asy'):
                runner.schedule(AsymptoteTask(base_logger, figure_path), trigger=str(path))

        if not fnmatch(path, 'output/notebook.pdf') and (
            fnmatch(path, 'notebook.tex') or
            fnmatch(path, 'classes/notebook.cls') or
            fnmatch(path, 'bibliography/*.bib') or
            fnmatch(path, 'text/*.tex') or
            fnmatch(path, 'images/*') or
            fnmatch(path, 'output/*') or
            fnmatch(path, 'packages/*.sty')
        ):
            runner.schedule(LaTeXTask(base_logger, ROOT_PATH / 'notebook.tex'), trigger=str(path))


@click.command()
@click.option('--no-aux', is_flag=True)
def watch(*, no_aux: bool) -> None:
    base_logger = structlog.get_logger().bind(logger='<system>')

    try:
        asyncio.run(setup_watchers(base_logger, no_aux=no_aux))
    except KeyboardInterrupt:
        base_logger.info('Gracefully shutting down')
