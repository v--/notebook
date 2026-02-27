import pytest
from coverage import Coverage


def get_coverage() -> None:
    cov = Coverage(omit=['test_*', 'conftest.py', '__init__.py', 'exceptions.py'])

    with cov.collect():
        pytest.console_main()

    cov.html_report()
