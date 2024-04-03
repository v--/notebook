import os.path

from loguru import logger
import pathlib

from .inflection import prefix_cardinal
from .formatting import Formatter
from .paths import ROOT_DIR
from .exceptions import NotebookCommandError


def bulk_format(path: pathlib.Path, glob_pattern: str, formatter_cls: type[Formatter]) -> None:
    if not path.is_absolute():
        path = ROOT_DIR / path

    total_count = 0
    formatted_count = 0

    if path.is_dir():
        for subpath in path.glob(glob_pattern):
            formatted_count += formatter_cls(os.path.join(path, subpath)).process()
            total_count += 1
    elif path.is_file():
        formatted_count += formatter_cls(path).process()
        total_count += 1
    else:
        raise NotebookCommandError(f'Cannot process path {repr(path.as_posix())}')

    logger.info(f'Processed {prefix_cardinal("file", total_count)}; {formatted_count} of them needed formatting.')
