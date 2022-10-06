import sys
import os

import pytest
from loguru import logger


@pytest.fixture(scope='session', autouse=True)
def execute_before_any_test():
    logger.remove()
    logger.add(
        sys.stdout,
        format='{message}',
        level=os.environ.get('LOGURU_LEVEL', default='INFO')
    )
