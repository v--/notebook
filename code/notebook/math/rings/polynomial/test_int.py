from ....support.pytest import pytest_parametrize_kwargs
from . import monomial
from .int import IntPolynomial, const, x, y, z, zero


@pytest_parametrize_kwargs(
    dict(p=zero,            degree=None),
    dict(p=const,           degree=0),
    dict(p=0 * const,       degree=None),
    dict(p=0 * x,           degree=None),
    dict(p=x * y,           degree=2),
    dict(p=2 * x ** 2,      degree=2),
    dict(p=x * y * z,       degree=3),
    dict(p=x * y * z ** 2,  degree=4),
)
def test_total_degree(p: IntPolynomial, degree: int) -> None:
    assert p.total_degree == degree


@pytest_parametrize_kwargs(
    dict(a=x, b=zero,  c=x),
    dict(a=x, b=y,     c=IntPolynomial.from_mapping({monomial.x: 1, monomial.y: 1})),
    dict(a=x, b=const, c=IntPolynomial.from_mapping({monomial.x: 1, monomial.const: 1})),
    dict(a=x, b=-x,    c=zero),
)
def test_add(a: IntPolynomial, b: IntPolynomial, c: IntPolynomial) -> None:
    assert a + b == c


@pytest_parametrize_kwargs(
    dict(p=zero,              expected='0'),
    dict(p=0 * const,         expected='0'),
    dict(p=const,             expected='1'),
    dict(p=2 * x,             expected='2x'),
    dict(p=-x,                expected='-x'),
    dict(p=-2 * x,            expected='-2x'),
    dict(p=x - y,             expected='x - y'),
    dict(p=x ** 2 - const,    expected='x² - 1'),
)
def test_str(p: IntPolynomial, expected: str) -> None:
    assert str(p) == expected
