import sys

import pytest


def run_benchmark() -> None:
    pytest.main(['--config-file', 'pytest_benchmark.ini', *sys.argv[1:]])
