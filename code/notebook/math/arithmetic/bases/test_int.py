from ....support.pytest import pytest_parametrize_kwargs
from ...polynomials.polynomial.int import IntPolynomial, const, x, zero
from .int import add_with_carrying, get_integer_expansion


@pytest_parametrize_kwargs(
    dict(n=0, radix=2, pol=zero),
    dict(n=1, radix=2, pol=const),
    dict(n=2, radix=2, pol=x),
    dict(n=3, radix=2, pol=x + const),
    dict(n=4, radix=2, pol=x ** 2),
    dict(n=5, radix=2, pol=x ** 2 + const),
    dict(n=8, radix=2, pol=x ** 3),
    dict(n=8, radix=3, pol=2 * (x + const)),
)
def test_integer_expansion(n: int, radix: int, pol: IntPolynomial) -> None:
    assert get_integer_expansion(n, radix).polynomial == pol


@pytest_parametrize_kwargs(
    dict(n=0, m=0, radix=10),
    dict(n=3, m=0, radix=2),
    dict(n=3, m=5, radix=2),
    dict(n=3, m=5, radix=10),
    dict(n=3, m=-5, radix=10),
    dict(n=-3, m=5, radix=10),
    dict(n=-3, m=-5, radix=10),
    dict(n=1, m=-9, radix=10),
    # dict(n=343, m=50315, radix=3),
    # dict(n=343, m=-50315, radix=3),
    # dict(n=-343, m=50315, radix=3),
    # dict(n=-343, m=-50315, radix=3),
)
def test_add_with_carrying(n: int, m: int, radix: int) -> None:
    assert add_with_carrying(n, m, radix) == n + m
