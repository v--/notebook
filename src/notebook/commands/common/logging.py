import logging

from rich.logging import RichHandler


class SubjectLoggerHandler(RichHandler):
    handler: logging.Handler
    handler = RichHandler(markup=True)

    def __init__(self) -> None:
        super().__init__(markup=True)
        self.setFormatter(
            logging.Formatter('[bold]%(subject)-15s[/]  %(message)s', defaults={'subject': '<system>'}),
        )
