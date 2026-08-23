import random
from collections.abc import Sequence

from notebook.math.arithmetic.divisibility import rem
from notebook.support.pytest import pytest_parametrize_kwargs, pytest_parametrize_lists, repeat5

from .gcd import ModularEquation, chinese_remainder_theorem_iteration, extended_gcd, gcd


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


@pytest_parametrize_kwargs(
    dict(
        equations=[ModularEquation(3, 4), ModularEquation(3, 5)],
        expected=3,
    ),
    dict(
        equations=[ModularEquation(3, 7), ModularEquation(4, 6), ModularEquation(0, 5)],
        expected=10,
    ),
)
def test_chinese_remainder_theorem_iteration(equations: Sequence[ModularEquation], expected: int) -> None:
    for eq in equations:
        assert rem(eq.value, eq.modulus) == rem(expected, eq.modulus)

    solution = chinese_remainder_theorem_iteration(equations)
    assert solution == expected
