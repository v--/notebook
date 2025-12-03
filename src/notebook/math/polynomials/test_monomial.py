from ...parsing import common_identifiers as ci
from ...support.pytest import pytest_parametrize_kwargs
from .monomial import Monomial


@pytest_parametrize_kwargs(
    dict(mon=Monomial({}),                 degree=0),
    dict(mon=Monomial({ci.x: 1}),             degree=1),
    dict(mon=Monomial({ci.x: 2}),             degree=2),
    dict(mon=Monomial({ci.x: 1, ci.y: 1}),       degree=2),
    dict(mon=Monomial({ci.x: 1, ci.y: 2, ci.z: 1}), degree=4),
)
def test_total_degree(mon: Monomial, degree: int) -> None:
    assert mon.degree == degree


@pytest_parametrize_kwargs(
    dict(a=Monomial({ci.x: 1}),       b=Monomial({})),
    dict(a=Monomial({ci.x: 2}),       b=Monomial({ci.x: 1})),
    dict(a=Monomial({ci.x: 1}),       b=Monomial({ci.y: 1})),
    dict(a=Monomial({ci.x: 1, ci.y: 2}), b=Monomial({ci.x: 1, ci.y: 1})),
    dict(a=Monomial({ci.x: 2, ci.y: 1}), b=Monomial({ci.x: 1, ci.y: 2})),
)
def test_ordering(a: Monomial, b: Monomial) -> None:
    assert a < b


@pytest_parametrize_kwargs(
    dict(a=Monomial({ci.x: 1}),       b=Monomial({}),           c=Monomial({ci.x: 1})),
    dict(a=Monomial({ci.x: 2}),       b=Monomial({ci.x: 1}),       c=Monomial({ci.x: 3})),
    dict(a=Monomial({ci.x: 1}),       b=Monomial({ci.y: 1}),       c=Monomial({ci.x: 1, ci.y: 1})),
    dict(a=Monomial({ci.x: 1, ci.y: 2}), b=Monomial({ci.x: 1, ci.y: 1}), c=Monomial({ci.x: 2, ci.y: 3})),
    dict(a=Monomial({ci.x: 2, ci.y: 1}), b=Monomial({ci.x: 1, ci.y: 2}), c=Monomial({ci.x: 3, ci.y: 3})),
)
def test_mult(a: Monomial, b: Monomial, c: Monomial) -> None:
    assert a * b == c
