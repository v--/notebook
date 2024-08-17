import random

import pytest

from .divisibility import extended_gcd, gcd, quot_dist, quot_floor, quot_max, quot_trunc


def test_quot_max() -> None:
    assert quot_max(10, 3) == 3
    assert quot_max(10, -3) == -3
    assert quot_max(-10, 3) == -4
    assert quot_max(-10, -3) == 4


def test_quot_dist() -> None:
    assert quot_dist(10, 3) == 3
    assert quot_dist(10, -3) == -3
    assert quot_dist(-10, 3) == -3
    assert quot_dist(-10, -3) == 3

    assert quot_dist(10, 12) == 1
    assert quot_dist(10, -12) == -1
    assert quot_dist(-10, 12) == -1
    assert quot_dist(-10, -12) == 1

    assert quot_dist(1, 2) == 0
    assert quot_dist(-1, 2) == 0
    assert quot_dist(3, 2) == 2
    assert quot_dist(-3, 2) == -2


def test_quot_trunc() -> None:
    assert quot_trunc(10, 3) == 3
    assert quot_trunc(10, -3) == -3
    assert quot_trunc(-10, 3) == -3
    assert quot_trunc(-10, -3) == 3

    assert quot_trunc(10, 12) == 0
    assert quot_trunc(10, -12) == 0
    assert quot_trunc(-10, 12) == 0
    assert quot_trunc(-10, -12) == 0

    assert quot_trunc(1, 2) == 0
    assert quot_trunc(-1, 2) == 0
    assert quot_trunc(3, 2) == 1
    assert quot_trunc(-3, 2) == -1

def test_quot_floor() -> None:
    assert quot_floor(10, 3) == 3 == 10 // 3
    assert quot_floor(10, -3) == -4 == 10 // -3
    assert quot_floor(-10, 3) == -4 == -10 // 3
    assert quot_floor(-10, -3) == 3 == -10 // -3


@pytest.mark.parametrize(('n', 'm'), [(random.randint(-100, 100), random.randint(-100, 100)) for _ in range(5)])
def test_gcd(n: int, m: int) -> None:
    g = max(k for k in range(1, max(abs(n), abs(m)) + 1) if n % k == 0 and m % k == 0)
    assert gcd(n, m) == g


@pytest.mark.parametrize(('n', 'm'), [(random.randint(-100, 100), random.randint(-100, 100)) for _ in range(5)])
def test_extended_gcd(n: int, m: int) -> None:
    g = max(k for k in range(1, max(abs(n), abs(m)) + 1) if n % k == 0 and m % k == 0)
    assert extended_gcd(n, m).gcd == g
