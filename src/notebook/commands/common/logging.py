import logging
from typing import TYPE_CHECKING

import colorlog

from notebook.support.iteration import string_accumulator


if TYPE_CHECKING:
    from collections.abc import Iterable


@string_accumulator(' ')
def get_format_string(log_subject: bool) -> Iterable[str]:
    yield '{green}{asctime}{reset} {bold}{log_color}{levelname:8}{reset}'

    if log_subject:
        yield '{cyan}{subject:15}{reset}'

    yield '{log_color}{message}{reset}'


class NotebookLoggerHandler(logging.StreamHandler):
    def __init__(self, log_subject: bool = False) -> None:
        super().__init__()
        self.setFormatter(
            colorlog.ColoredFormatter(
                style='{',
                fmt=get_format_string(log_subject),
                datefmt='%X',
                defaults={'subject': '<system>'},
                log_colors={**colorlog.default_log_colors, 'INFO': 'white'},
            ),
        )
