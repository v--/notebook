import pathlib

import structlog

from .exceptions import NotebookCommandError
from .formatting import Formatter
from .inflection import prefix_cardinal
from .paths import ROOT_PATH


def bulk_format(path: pathlib.Path, glob_pattern: str, formatter_cls: type[Formatter]) -> None:
    base_logger = structlog.get_logger().bind(logger=path)

    if not path.is_absolute():
        path = ROOT_PATH / path

    total_count = 0
    formatted_count = 0

    if path.is_dir():
        for subpath in path.glob(glob_pattern):
            formatted_count += formatter_cls(base_logger.bind(logger=subpath), subpath).process()
            total_count += 1
    elif path.is_file():
        formatted_count += formatter_cls(base_logger, path).process()
        total_count += 1
    else:
        raise NotebookCommandError(f'Cannot process path {path.as_posix()!r}')

    base_logger.info(f'Processed {prefix_cardinal("file", total_count)}; {formatted_count} of them needed formatting.')
