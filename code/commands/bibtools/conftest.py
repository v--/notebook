import loguru
import pytest
import pytest_loguru.plugin


@pytest.fixture(autouse=True)
def disable_loguru() -> None:
    loguru.logger.remove()
