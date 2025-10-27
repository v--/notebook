from ...support.pytest import pytest_parametrize_kwargs
from .monomial import Monomial


@pytest_parametrize_kwargs(
    dict(mon=Monomial(),              degree=0),
    dict(mon=Monomial(x=1),           degree=1),
    dict(mon=Monomial(x=2),           degree=2),
    dict(mon=Monomial(x=1, y=1),      degree=2),
    dict(mon=Monomial(x=1, y=2, Z=1), degree=4),
)
def test_total_degree(mon: Monomial, degree: int) -> None:
    assert mon.total_degree == degree


@pytest_parametrize_kwargs(
    dict(a=Monomial(x=1),      b=Monomial()),
    dict(a=Monomial(x=2),      b=Monomial(x=1)),
    dict(a=Monomial(x=1),      b=Monomial(y=1)),
    dict(a=Monomial(x=1, y=2), b=Monomial(x=1, y=1)),
    dict(a=Monomial(x=2, y=1), b=Monomial(x=1, y=2)),
)
def test_ordering(a: Monomial, b: Monomial) -> None:
    assert a < b


@pytest_parametrize_kwargs(
    dict(a=Monomial(x=1),      b=Monomial(),         c=Monomial(x=1)),
    dict(a=Monomial(x=2),      b=Monomial(x=1),      c=Monomial(x=3)),
    dict(a=Monomial(x=1),      b=Monomial(y=1),      c=Monomial(x=1, y=1)),
    dict(a=Monomial(x=1, y=2), b=Monomial(x=1, y=1), c=Monomial(x=2, y=3)),
    dict(a=Monomial(x=2, y=1), b=Monomial(x=1, y=2), c=Monomial(x=3, y=3)),
)
def test_mult(a: Monomial, b: Monomial, c: Monomial) -> None:
    assert a * b == c
