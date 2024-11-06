
from ...support.pytest import pytest_parametrize_kwargs
from .divisibility import quot_dist, quot_floor, quot_max, quot_trunc


@pytest_parametrize_kwargs(
    dict(n=10,  m=3,  max_=3,  dist=3,  trunc=3,  floor=3),
    dict(n=10,  m=-3, max_=-3, dist=-3, trunc=-3, floor=-4),
    dict(n=-10, m=3,  max_=-4, dist=-3, trunc=-3, floor=-4),
    dict(n=-10, m=-3, max_=4,  dist=3,  trunc=3,  floor=3),
)
def test_quot_basic(n: int, m: int, max_: int, dist: int, trunc: int, floor: int) -> None:
    assert quot_max(n, m) == max_
    assert quot_dist(n, m) == dist
    assert quot_trunc(n, m) == trunc
    assert quot_floor(n, m) == floor


@pytest_parametrize_kwargs(
    dict(n=10,  m=12,  dist=1,  trunc=0),
    dict(n=10,  m=-12, dist=-1, trunc=0),
    dict(n=-10, m=12,  dist=-1, trunc=0),
    dict(n=-10, m=-12, dist=1,  trunc=0),

    dict(n=1,   m=12,  dist=0,  trunc=0),
    dict(n=-1,  m=-12, dist=0,  trunc=0),

    dict(n=3,   m=2,   dist=2,  trunc=1),
    dict(n=3,   m=-2,  dist=-2, trunc=-1),
    dict(n=-3,  m=2,   dist=-2, trunc=-1),
    dict(n=-3,  m=-2,  dist=2,  trunc=1),
)
def test_quot_dist(n: int, m: int, dist: int, trunc: int) -> None:
    assert quot_dist(n, m) == dist
    assert quot_trunc(n, m) == trunc
