import random

import pytest

from ..linalg.matrix import eye, fill
from .tropical import MinPlusFloat, TropicalDivisionError, TropicalSubtractionError


@pytest.mark.parametrize(
    ('a', 'b'),
    [(random.uniform(-100, 100), random.uniform(-100, 100)) for _ in range(5)]
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
    assert t @ t == fill(n, dtype=MinPlusFloat, value=float('inf'))
