import loguru
import pytest
import pytest_loguru.plugin  # noqa: F401


@pytest.fixture(autouse=True)
def disable_loguru() -> None:
    loguru.logger.remove()
