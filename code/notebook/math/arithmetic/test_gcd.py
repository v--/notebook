import random

from ...support.pytest import pytest_parametrize_lists, repeat5
from .gcd import extended_gcd, gcd


@pytest_parametrize_lists(
    n=repeat5(random.randint, -100, 100),
    m=repeat5(random.randint, -100, 100),
)
def test_gcd(n: int, m: int) -> None:
    g = max(k for k in range(1, max(abs(n), abs(m)) + 1) if n % k == 0 and m % k == 0)
    assert gcd(n, m) == g


@pytest_parametrize_lists(
    n=repeat5(random.randint, -100, 100),
    m=repeat5(random.randint, -100, 100),
)
def test_extended_gcd(n: int, m: int) -> None:
    g = max(k for k in range(1, max(abs(n), abs(m)) + 1) if n % k == 0 and m % k == 0)
    assert extended_gcd(n, m).gcd == g
