import sys

from loguru import logger


def configure_loguru(*, verbose: bool) -> None:
    logger.remove()
    logger.configure(extra=dict(logger='<system>'))
    logger.add(
        sys.stdout,
        format='<level>{level:8}</level> <green>{time:HH:mm:ss}</green>   <cyan>{extra[logger]}</cyan>   <level>{message}</level>',
        level='DEBUG' if verbose else 'INFO'
    )
