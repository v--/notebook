from collections.abc import Mapping

import pytest

from ....support.pytest import pytest_parametrize_kwargs
from .. import monomial
from ..exceptions import PolynomialEvaluationError
from .int import IntPolynomial, const, x, y, z, zero


@pytest_parametrize_kwargs(
    dict(pol=const,           degree=0),
    dict(pol=x * y,           degree=2),
    dict(pol=2 * x ** 2,      degree=2),
    dict(pol=x * y * z,       degree=3),
    dict(pol=x * y * z ** 2,  degree=4),
)
def test_total_degree(pol: IntPolynomial, degree: int) -> None:
    assert pol.total_degree == degree


@pytest_parametrize_kwargs(
    dict(pol=const,                                 indet='x', leading=const),
    dict(pol=x ** 2,                                indet='x', leading=const),
    dict(pol=x - 2 * x ** 2,                        indet='x', leading=-2 * const),
    dict(pol=x * y,                                 indet='x', leading=y),
    dict(pol=x * y,                                 indet='y', leading=x),
    dict(pol=x ** 2 * y + 2 * (x ** 2) * z + x * y, indet='x', leading=y + 2 * z),
)
def test_leading_coefficient(pol: IntPolynomial, indet: str, leading: IntPolynomial) -> None:
    assert pol.leading_coefficient(indet) == leading


@pytest_parametrize_kwargs(
    dict(a=x, b=zero,  c=x),
    dict(a=x, b=y,     c=IntPolynomial.from_mapping({monomial.x: 1, monomial.y: 1})),
    dict(a=x, b=const, c=IntPolynomial.from_mapping({monomial.x: 1, monomial.const: 1})),
    dict(a=x, b=-x,    c=zero),
)
def test_add(a: IntPolynomial, b: IntPolynomial, c: IntPolynomial) -> None:
    assert a + b == c


@pytest_parametrize_kwargs(
    dict(pol=zero,              expected='0'),
    dict(pol=0 * const,         expected='0'),
    dict(pol=const,             expected='1'),
    dict(pol=2 * x,             expected='2x'),
    dict(pol=-x,                expected='-x'),
    dict(pol=-2 * x,            expected='-2x'),
    dict(pol=x - y,             expected='x - y'),
    dict(pol=x ** 2 - const,    expected='x² - 1'),
)
def test_str(pol: IntPolynomial, expected: str) -> None:
    assert str(pol) == expected


@pytest_parametrize_kwargs(
    dict(pol=zero,       e=dict(),         expected=0),
    dict(pol=0 * const,  e=dict(),         expected=0),
    dict(pol=x,          e=dict(x=3),      expected=3),
    dict(pol=2 * x ** 2, e=dict(x=3),      expected=18),
    dict(pol=2 * x * y,  e=dict(x=3, y=2), expected=12),
)
def test_call(pol: IntPolynomial, e: Mapping[str, int], expected: int) -> None:
    assert pol(**e) == expected


def test_call_failure() -> None:
    with pytest.raises(PolynomialEvaluationError):
        assert x(y=2)
