import random

import pytest

from ...support.pytest import pytest_parametrize_lists, repeat5
from ..linalg.matrix import eye
from .tropical import MinPlusFloat, TropicalDivisionError, TropicalSubtractionError


@pytest_parametrize_lists(
    a=repeat5(random.uniform, -100, 100),
    b=repeat5(random.uniform, -100, 100),
)
def test_tropical_arithmetic(a: float, b: float) -> None:
    assert MinPlusFloat(a) + b == min(a, b)
    assert MinPlusFloat(a) * b == a + b

    with pytest.raises(TropicalSubtractionError):
        MinPlusFloat(a) - b

    with pytest.raises(TropicalDivisionError):
        MinPlusFloat(a) / b

    assert a + MinPlusFloat(b) == min(a, b)
    assert a * MinPlusFloat(b) == a + b

    with pytest.raises(TropicalSubtractionError):
        a - MinPlusFloat(b)

    with pytest.raises(TropicalDivisionError):
        a / MinPlusFloat(b)


def test_matrix_arithmetic(n: int = 3) -> None:
    t = eye(n, dtype=MinPlusFloat, diag=0.0, off_diag=float('inf'))
    assert t + t == t
    assert t @ t == t
