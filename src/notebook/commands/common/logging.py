import sys

import loguru


def configure_loguru(*, verbose: bool) -> None:
    loguru.logger.configure(extra=dict(logger='<system>'))
    loguru.logger.remove()
    loguru.logger.add(
        sys.stdout,
        format='<level>{level:7}</level> <green>{time:HH:mm:ss}</green>   <cyan>{extra[logger]}</cyan> <level>{message}</level>',
        level='DEBUG' if verbose else 'INFO'
    )
