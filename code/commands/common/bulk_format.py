import pathlib
from collections.abc import Sequence

import loguru

from ..common.inflection import prefix_cardinal
from .formatting import Formatter


def bulk_format(paths: Sequence[pathlib.Path], formatter_cls: type[Formatter]) -> None:
    base_logger = loguru.logger

    total_count = 0
    formatted_count = 0

    for path in paths:
        formatted_count += formatter_cls(base_logger.bind(logger=path.name), path).process()
        total_count += 1

    base_logger.info(f'Processed {prefix_cardinal("file", total_count)}; {formatted_count} of them needed formatting.')
