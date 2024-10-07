import itertools
import random
import re
from fractions import Fraction

import pytest

from ...support.pytest import pytest_parametrize_kwargs, pytest_parametrize_lists, repeat5
from .bases import get_digit, get_digit_rational, get_fraction, get_number_expansion, get_rational_number_expansion


@pytest_parametrize_lists(
    x=repeat5(random.uniform, -1, 1),
    radix=repeat5(random.choice, [2, 3, 8, 10]),
)
def test_get_digit(x: float, radix: int, precision: int = 10) -> None:
    digits = [get_digit(x=x, radix=radix, index=k) for k in range(precision + 1)]
    reconstructed = sum(d * radix ** (-k) for k, d in enumerate(digits))
    assert reconstructed == pytest.approx(x, abs=radix ** -precision)


# Works only on fractional digits
@pytest_parametrize_lists(
    p=repeat5(random.randint, 0, 10),
    q=repeat5(random.randint, 11, 20),
    radix=repeat5(random.choice, [2, 3, 8, 10]),
)
def test_get_rational_digit(p: int, q: int, radix: int, precision: int = 10) -> None:
    digits = [get_digit_rational(p=p, q=q, radix=radix, index=k) for k in range(1, precision + 2)]
    reconstructed = sum(d * radix ** (-k-1) for k, d in enumerate(digits))
    assert reconstructed == pytest.approx(p / q, abs=radix ** -precision)


@pytest_parametrize_lists(
    x=repeat5(random.uniform, -100, 100),
    radix=repeat5(random.choice, [10, 16]),
)
def test_get_number_expansion(x: float, radix: int, precision: int = 10) -> None:
    e = get_number_expansion(x, radix=radix)
    assert float(e) == pytest.approx(x, abs=radix ** -precision)


@pytest_parametrize_lists(
    p=itertools.chain(
        [1] * 25,
        repeat5(random.randint, -1000, 1000)
    ),
    q=itertools.chain(
        range(1, 26),
        repeat5(random.randint, 1, 200)
    ),
    radix=itertools.chain(
        [10] * 25,
        repeat5(random.choice, [10, 16])
    ),
)
def test_get_rational_number_expansion(p: int, q: int, radix: int, precision: int = 10) -> None:
    frac = Fraction(p, q)
    e = get_rational_number_expansion(frac, radix=radix)
    assert float(e) == pytest.approx(p / q, abs=radix ** -precision)

    match = re.match(r'(?P<int>-?[\dA-Z]+)(\.(?P<frac>[\dA-Z]*)(\((?P<rep>[\dA-Z]+)\))?)?', str(e))
    assert match
    assert int(match.group('int'), base=radix) == pytest.approx(p / q, abs=1)


@pytest_parametrize_lists(
    p=itertools.chain(
        [1] * 15,
        repeat5(random.randint, -100, 100)
    ),
    q=itertools.chain(
        range(1, 16),
        repeat5(random.randint, 1, 15)
    ),
    radix=itertools.chain(
        [10] * 15,
        repeat5(random.choice, [10, 16])
    ),
)
def test_get_fraction(p: int, q: int, radix: int) -> None:
    frac = Fraction(p, q)
    e = get_rational_number_expansion(frac, radix=radix)
    assert frac == get_fraction(e)


@pytest_parametrize_kwargs(
    dict(frac=Fraction(1, 7),   radix=10, expected='0.(142857)'),
    dict(frac=Fraction(10, 7),  radix=10, expected='1.(428571)'),
    dict(frac=Fraction(100, 7), radix=10, expected='14.(285714)'),
    dict(frac=Fraction(1, 70),  radix=10, expected='0.0(142857)'),
    dict(frac=Fraction(1, 700), radix=10, expected='0.00(142857)'),

    dict(frac=Fraction(3, 1),   radix=10, expected='3'),
    dict(frac=Fraction(3, 1),   radix=3,  expected='10'),

    dict(frac=Fraction(1, 3),   radix=10, expected='0.(33)'),
    dict(frac=Fraction(1, 3),   radix=3,  expected='0.1'),
    dict(frac=Fraction(1, 9),   radix=3,  expected='0.01'),

    dict(frac=Fraction(10, 3),  radix=10, expected='3.(33)'),
    dict(frac=Fraction(10, 3),  radix=3,  expected='10.1'),

    dict(frac=Fraction(100, 3), radix=10, expected='33.(33)'),
    dict(frac=Fraction(100, 3), radix=3,  expected='1020.1'),

    dict(frac=Fraction(1, 30),  radix=10, expected='0.0(33)'),
    dict(frac=Fraction(1, 30),  radix=3,  expected='0.0(0022)'),

    dict(frac=Fraction(1, 300), radix=10, expected='0.00(33)'),
    dict(frac=Fraction(1, 300), radix=3,  expected='0.0(0000210212111020012200002102121110200100)')
)
def test_get_rational_number_expansion_strings(frac: Fraction, radix: int, expected: str) -> None:
    e = get_rational_number_expansion(frac, radix=radix)
    assert str(e) == expected
