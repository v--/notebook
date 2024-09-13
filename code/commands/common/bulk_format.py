import pathlib

import loguru

from ..common.inflection import prefix_cardinal
from .formatting import Formatter


def bulk_format(formatter_cls: type[Formatter], *paths: pathlib.Path) -> None:
    base_logger = loguru.logger

    total_count = 0
    formatted_count = 0

    for path in paths:
        formatted_count += formatter_cls(base_logger.bind(logger=path.name), path).process()
        total_count += 1

    base_logger.info(f'Processed {prefix_cardinal("file", total_count)}; {formatted_count} of them needed formatting.')
