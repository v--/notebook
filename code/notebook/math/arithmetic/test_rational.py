import random
from fractions import Fraction

from ...support.pytest import pytest_parametrize_lists, repeat5
from .rational import power_bisection


@pytest_parametrize_lists(
    a=repeat5(random.randint, 1, 200),
    b=repeat5(random.randint, 10, 20),
    c=repeat5(random.randint, 300, 500),
    d=repeat5(random.randint, 5, 10),
    n=repeat5(random.randint, 2, 5),
)
def test_power_bisection(a: int, b: int, c: int, d: int, n: int) -> None:
    x = Fraction(a, b)
    y = Fraction(c, d)
    assert x < power_bisection(x, y, n) ** n < y
