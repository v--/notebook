import asyncio
import os.path
from fnmatch import fnmatch
from typing import AsyncIterator, Literal, get_args

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
        inotify.add_watch(ROOT_PATH / 'bibliography', Mask.MODIFY)
        inotify.add_watch(ROOT_PATH / 'asymptote', Mask.MODIFY)
        inotify.add_watch(ROOT_PATH / 'classes', Mask.MODIFY)
        inotify.add_watch(ROOT_PATH / 'output', Mask.MODIFY)
        logger.info('Started daemon and initialized watchers')

        async for event in inotify:
            if event.path is not None:
                yield os.path.relpath(event.path, ROOT_PATH)


async def setup_watchers(target: WatchTarget, base_logger: structlog.stdlib.BoundLogger) -> None:
    runner = TaskRunner()

    async for path in iter_file_changes(base_logger):
        if target == 'all' or target == 'figures':
            if fnmatch(path, 'classes/tikzcd.cls') or fnmatch(path, 'classes/forest.cls') or fnmatch(path, 'packages/*.sty'):
                for figure_path in FIGURES_PATH.glob('*.tex'):
                    runner.schedule(LaTeXTask(base_logger, figure_path), trigger=str(path))

            if fnmatch(path, 'figures/*.tex'):
                runner.schedule(LaTeXTask(base_logger, path), trigger=str(path))

            if fnmatch(path, 'figures/*.asy'):
                runner.schedule(AsymptoteTask(base_logger, path), trigger=str(path))

            if fnmatch(path, 'asymptote/*.asy'):
                for figure_path in FIGURES_PATH.glob('*.asy'):
                    runner.schedule(AsymptoteTask(base_logger, figure_path), trigger=str(path))

        if (target == 'all' or target == 'notebook') and not fnmatch(path, 'output/notebook.pdf') and (
            fnmatch(path, 'notebook.tex') or
            fnmatch(path, 'classes/notebook.cls') or
            fnmatch(path, 'bibliography/*.bib') or
            fnmatch(path, 'text/*.tex') or
            fnmatch(path, 'output/*.pdf') or
            fnmatch(path, 'packages/*.sty')
        ):
            runner.schedule(LaTeXTask(base_logger, ROOT_PATH / 'notebook.tex'), trigger=str(path))


@click.command()
@click.argument('target', type=click.Choice(get_args(WatchTarget)))
def watch(target: WatchTarget) -> None:
    base_logger = structlog.get_logger().bind(logger='<system>')

    try:
        asyncio.run(setup_watchers(target, base_logger))
    except KeyboardInterrupt:
        base_logger.info('Gracefully shutting down')
