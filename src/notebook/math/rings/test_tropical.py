import random

import pytest

from ...support.pytest import pytest_parametrize_lists, repeat5
from .tropical import MinPlusFloat


@pytest_parametrize_lists(
    a=repeat5(random.uniform, -100, 100),
    b=repeat5(random.uniform, -100, 100),
)
def test_tropical_sum(a: float, b: float) -> None:
    assert float(MinPlusFloat(a) + MinPlusFloat(b)) == pytest.approx(min(a, b))


@pytest_parametrize_lists(
    a=repeat5(random.uniform, -100, 100),
    b=repeat5(random.uniform, -100, 100),
)
def test_tropical_prod(a: float, b: float) -> None:
    assert float(MinPlusFloat(a) * MinPlusFloat(b)) == pytest.approx(a + b)
