from ...support.pytest import pytest_parametrize_kwargs
from .modular import Z3


@pytest_parametrize_kwargs(
    dict(n=0,  expected=Z3(0)),
    dict(n=1,  expected=Z3(1)),
    dict(n=2,  expected=Z3(2)),
    dict(n=3,  expected=Z3(0)),
    dict(n=4,  expected=Z3(1)),
    dict(n=-1, expected=Z3(2)),
    dict(n=-2, expected=Z3(1)),
    dict(n=-3, expected=Z3(0)),
    dict(n=-4, expected=Z3(2)),
)
def test_z3_init(n: int, expected: Z3) -> None:
    assert Z3(n) == expected


@pytest_parametrize_kwargs(
    dict(n=0,  m=0,  expected=Z3(0)),
    dict(n=1,  m=1,  expected=Z3(2)),
    dict(n=1,  m=2,  expected=Z3(0)),
    dict(n=-1, m=-1, expected=Z3(1)),
)
def test_z3_addition(n: int, m: int, expected: Z3) -> None:
    assert Z3(n) + Z3(m) == expected


@pytest_parametrize_kwargs(
    dict(n=0,  m=0, expected=Z3(0)),
    dict(n=1,  m=1, expected=Z3(1)),
    dict(n=1,  m=2, expected=Z3(2)),
    dict(n=-1, m=1, expected=Z3(2)),
)
def test_z3_multiplication(n: int, m: int, expected: Z3) -> None:
    assert Z3(n) * Z3(m) == expected
