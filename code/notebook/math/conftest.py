import os
import sys

import pytest
from loguru import logger


@pytest.fixture(scope='session', autouse=True)
def _execute_before_any_test() -> None:
    logger.remove()
    logger.add(
        sys.stdout,
        format='{message}',
        level=os.environ.get('LOGURU_LEVEL', default='INFO')
    )
