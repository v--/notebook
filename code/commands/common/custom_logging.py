import sys

from loguru import logger


def setup_loguru(default_name: str = '<system>'):
    logger.configure(extra=dict(name=default_name))
    logger.remove()
    logger.add(
        sys.stdout,
        colorize=True,
        format='<green>{time:HH:mm:ss}</green> | <level>{level:7}</level> | {extra[name]} | <level>{message}</level>',
    )
