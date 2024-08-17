import random
import re
from fractions import Fraction

import pytest

from .bases import get_digit, get_digit_rational, get_fraction, get_number_expansion, get_rational_number_expansion


@pytest.mark.parametrize(('x', 'radix'), [(random.uniform(-1, 1), random.choice([2, 3, 8, 10])) for _ in range(5)])
def test_get_digit(x: float, radix: int, precision: int = 10) -> None:
    digits = [get_digit(x=x, radix=radix, index=k) for k in range(precision + 1)]
    reconstructed = sum(d * radix ** (-k) for k, d in enumerate(digits))
    assert reconstructed == pytest.approx(x, abs=radix ** -precision)


# Works only on fractional digits
@pytest.mark.parametrize(('p', 'q', 'radix'), [(random.randint(0, 10), random.randint(11, 20), random.choice([2, 3, 8, 10])) for _ in range(5)])
def test_get_rational_digit(p: int, q: int, radix: int, precision: int = 10) -> None:
    digits = [get_digit_rational(p=p, q=q, radix=radix, index=k) for k in range(1, precision + 2)]
    reconstructed = sum(d * radix ** (-k-1) for k, d in enumerate(digits))
    assert reconstructed == pytest.approx(p / q, abs=radix ** -precision)


@pytest.mark.parametrize(('x', 'radix'), [(random.uniform(-100, 100), random.choice([10, 16])) for _ in range(5)])
def test_get_number_expansion(x: float, radix: int, precision: int = 10) -> None:
    e = get_number_expansion(x, radix=radix)
    assert float(e) == pytest.approx(x, abs=radix ** -precision)


@pytest.mark.parametrize(
    ('p', 'q', 'radix'),
    [(1, q, 10) for q in range(1, 25)] + \
    [(random.randint(-1000, 1000), random.randint(1, 200), random.choice([10, 16])) for _ in range(5)]
)
def test_get_rational_number_expansion(p: int, q: int, radix: int, precision: int = 10) -> None:
    frac = Fraction(p, q)
    e = get_rational_number_expansion(frac, radix=radix)
    assert float(e) == pytest.approx(p / q, abs=radix ** -precision)

    match = re.match(r'(?P<int>-?[\dA-Z]+)(\.(?P<frac>[\dA-Z]*)(\((?P<rep>[\dA-Z]+)\))?)?', str(e))
    assert match
    assert int(match.group('int'), base=radix) == pytest.approx(p / q, abs=1)


@pytest.mark.parametrize(
    ('p', 'q', 'radix'),
    [(1, q, 10) for q in range(1, 15)] + \
    [(random.randint(-100, 100), random.randint(1, 15), random.choice([10, 16])) for _ in range(5)]
)
def test_get_fraction(p: int, q: int, radix: int) -> None:
    frac = Fraction(p, q)
    e = get_rational_number_expansion(frac, radix=radix)
    assert frac == get_fraction(e)


@pytest.mark.parametrize(
    ('frac', 'radix', 'string'),
    [
        (Fraction(1, 7),   10, '0.(142857)'),
        (Fraction(10, 7),  10, '1.(428571)'),
        (Fraction(100, 7), 10, '14.(285714)'),
        (Fraction(1, 70),  10, '0.0(142857)'),
        (Fraction(1, 700), 10, '0.00(142857)'),

        (Fraction(3, 1),   10, '3'),
        (Fraction(3, 1),   3,  '10'),

        (Fraction(1, 3),   10, '0.(33)'),
        (Fraction(1, 3),   3,  '0.1'),
        (Fraction(1, 9),   3,  '0.01'),

        (Fraction(10, 3),  10, '3.(33)'),
        (Fraction(10, 3),  3,  '10.1'),

        (Fraction(100, 3), 10, '33.(33)'),
        (Fraction(100, 3), 3,  '1020.1'),

        (Fraction(1, 30),  10, '0.0(33)'),
        (Fraction(1, 30),  3,  '0.0(0022)'),

        (Fraction(1, 300), 10, '0.00(33)'),
        (Fraction(1, 300), 3,  '0.0(0000210212111020012200002102121110200100)')
    ]
)
def test_get_rational_number_expansion_strings(frac: Fraction, radix: int, string: str) -> None:
    e = get_rational_number_expansion(frac, radix=radix)
    assert str(e) == string
