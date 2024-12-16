from ....support.pytest import pytest_parametrize_kwargs
from ...polynomials.polynomial.int import IntPolynomial, const, x, zero
from ..divisibility import quot, rem
from ..support import sgn
from .int import (
    IntRadixExpansion,
    add_with_carrying,
    get_integer_expansion,
    long_division,
    multi_digit_mult_with_carrying,
    single_digit_mult_with_carrying,
)


@pytest_parametrize_kwargs(
    dict(n=0,  radix=2, pol=zero),
    dict(n=1,  radix=2, pol=const),
    dict(n=2,  radix=2, pol=x),
    dict(n=3,  radix=2, pol=x + const),
    dict(n=4,  radix=2, pol=x ** 2),
    dict(n=5,  radix=2, pol=x ** 2 + const),
    dict(n=8,  radix=2, pol=x ** 3),
    dict(n=-8, radix=2, pol=x ** 3),
    dict(n=8,  radix=3, pol=2 * (x + const)),
)
def test_integer_expansion(n: int, radix: int, pol: IntPolynomial) -> None:
    assert get_integer_expansion(n, radix) == IntRadixExpansion(radix, pol, sgn(n))


@pytest_parametrize_kwargs(
    dict(n=0, m=0, radix=10),
    dict(n=3, m=0, radix=2),
    dict(n=3, m=5, radix=2),
    dict(n=3, m=5, radix=10),
    dict(n=3, m=-5, radix=10),
    dict(n=-3, m=5, radix=10),
    dict(n=-3, m=-5, radix=10),
    dict(n=1, m=-9, radix=10),
    dict(n=343, m=50315, radix=3),
    dict(n=343, m=-50315, radix=3),
    dict(n=-343, m=50315, radix=3),
    dict(n=-343, m=-50315, radix=3),
)
def test_add_with_carrying(n: int, m: int, radix: int) -> None:
    n_ = get_integer_expansion(n, radix)
    m_ = get_integer_expansion(m, radix)
    result = add_with_carrying(n_, m_)

    assert int(result) == n + m


@pytest_parametrize_kwargs(
    dict(n=0, m=0, radix=10),
    dict(n=3, m=0, radix=2),
    dict(n=3, m=5, radix=10),
    dict(n=3, m=-5, radix=10),
    dict(n=-3, m=5, radix=10),
    dict(n=-3, m=-5, radix=10),
    dict(n=1, m=-9, radix=10)
)
def test_single_digit_mult_with_carrying(n: int, m: int, radix: int) -> None:
    n_ = get_integer_expansion(n, radix)
    result = single_digit_mult_with_carrying(n_, m)
    assert int(result) == n * m


@pytest_parametrize_kwargs(
    dict(n=343, m=50315, radix=3),
    dict(n=343, m=-50315, radix=3),
    dict(n=-343, m=50315, radix=3),
    dict(n=-343, m=-50315, radix=3),
)
def test_multi_digit_mult_with_carrying(n: int, m: int, radix: int) -> None:
    n_ = get_integer_expansion(n, radix)
    m_ = get_integer_expansion(m, radix)
    result = multi_digit_mult_with_carrying(n_, m_)
    assert int(result) == n * m


@pytest_parametrize_kwargs(
    dict(n=1, m=2, radix=10),
    dict(n=2, m=2, radix=10),
    dict(n=19, m=3, radix=10),
    dict(n=21, m=3, radix=10),
    dict(n=50315,  m=343,  radix=10),
    dict(n=-50315, m=343,  radix=10),
    dict(n=50315,  m=-343, radix=10),
    dict(n=-50315, m=-343, radix=10),
)
def test_long_division(n: int, m: int, radix: int) -> None:
    n_ = get_integer_expansion(n, radix)
    m_ = get_integer_expansion(m, radix)
    q, r = long_division(n_, m_)
    assert int(q) == quot(n, m)
    assert int(r) == rem(n, m)
