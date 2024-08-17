import itertools
import math
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction

from .divisibility import divides, quot, rem
from .primes import factor, totient
from .support import SignT, sgn


# This is eq:alg:real_number_radix_expansion/direct in the monograph
def get_digit(x: float, radix: int, index: int) -> int:
    if x < 0:
        return -get_digit(-x, radix, index)

    return rem(math.floor(x * radix ** index), radix)


# This is eq:thm:alg:real_number_radix_expansion/rational_coefficient in the monograph
def get_digit_rational(p: int, q: int, radix: int, index: int) -> int:
    assert index > 0
    assert q > 0

    if p < 0:
        return -get_digit_rational(-p, q, radix, index)

    return quot(radix ** index * p, q) - radix * quot(radix ** (index - 1) * p, q)


def number_to_digit(n: int) -> str:
    assert n >= 0

    if n < 10:
        return str(n)

    if n < 36:
        return chr(ord('A') + (n - 10))

    raise ValueError(f'What digit corresponds to {n}?')


@dataclass
class RadixExpansion:
    radix: int
    max_power: int
    digits: Sequence[int]
    periodic_digits: Sequence[int]
    sign: SignT

    def __post_init__(self) -> None:
        if self.max_power + 1 > len(self.digits):
            raise ValueError('The number of digits explicitly provided must exceed the maximum power')

        if len(self.digits) == 0:
            raise ValueError('At least one digit expected')

        for i, d in enumerate(self.digits):
            if d < 0 or d >= self.radix:
                raise ValueError(f'Digit {d} at position {i} is out of bounds')

        if len(self.periodic_digits) == 0:
            raise ValueError('At least one periodic digit expected; possibly zero')

        for i, d in enumerate(self.periodic_digits):
            if d < 0 or d >= self.radix:
                raise ValueError(f'Periodic digit {d} at position {i} is out of bounds')

    def get_shift(self) -> int:
        return len(self.digits) - self.max_power - 1

    def is_period_zero(self) -> bool:
        return all(d == 0 for d in self.periodic_digits)

    def is_integer(self) -> bool:
        return self.get_shift() == 0 and all(d == 0 for d in self.periodic_digits)

    def __getitem__(self, index: int) -> int:
        if index < -self.max_power:
            return 0

        if index < -self.max_power + len(self.digits):
            return self.digits[self.max_power + index]

        # This is used for conversion to floats, but not for strings
        return self.periodic_digits[rem(self.max_power + index - len(self.digits), len(self.periodic_digits))]

    def __str__(self) -> str:
        result = ''.join(number_to_digit(self[k]) for k in range(min(0, -self.max_power), 1))

        if not self.is_integer():
            result += '.'

        result += ''.join(number_to_digit(self[k + 1]) for k in range(self.get_shift()))

        if not self.is_period_zero():
            result += '(' + ''.join(number_to_digit(d) for d in self.periodic_digits) + ')'

        if self.sign >= 0:
            return result

        return '-' + result

    def __float__(self) -> float:
        result = 0.0
        k = -self.max_power
        exp = self.radix ** (-k)

        while exp > sys.float_info.epsilon:
            result += self[k] * exp
            k += 1
            exp /= self.radix

        return self.sign * result


# This is alg:real_number_radix_expansion in the monograph
def get_number_expansion(x: int | float, radix: int) -> RadixExpansion:
    x_ = abs(x)

    max_power = max(itertools.takewhile(lambda k: radix ** k <= x_, itertools.count())) if x_ >= 1 else 0
    digits: list[int] = []
    s_k = 0  # s_{-m-1}

    for k in itertools.count(start=-max_power):
        # If not for floating-point shenanigans, this could have been written as
        # >>> math.floor(radix ** k * x_) - radix ** k * s_k
        d = min(radix - 1, math.floor(radix ** k * (x_ - s_k)))
        digits.append(d)
        s_k += d / radix ** k

        if (k > 0 and x_ - s_k < sys.float_info.epsilon) or (isinstance(x, int) and k == 0):
            break

    return RadixExpansion(radix=radix, max_power=max_power, digits=digits, sign=sgn(x), periodic_digits=[0])


# This is alg:rational_number_to_positional_string in the monograph
def get_rational_number_expansion(frac: Fraction, radix: int) -> RadixExpansion:
    p, q = frac.as_integer_ratio()
    q_factorization = factor(q)

    q_ = math.prod(
        p ** k for p, k in q_factorization.multiset.items()
        if not divides(p, radix)
    )

    r = quot(q, q_, raise_if_inexact=True)

    shift = next(
        k for k in itertools.count(start=0)
        if divides(r, radix ** k)
    )

    p_ = quot(abs(p) * radix ** shift, r, raise_if_inexact=True)

    int_part = quot(p_, q_)
    int_expansion = get_number_expansion(int_part, radix=radix)

    period = totient(q_)
    c = quot(radix ** period - 1, q_, raise_if_inexact=True)
    rep_expansion = get_number_expansion(c * rem(p_, q_), radix=radix)

    return RadixExpansion(
        radix=radix,
        periodic_digits=[0] * max(0, period - rep_expansion.max_power - 1) + list(rep_expansion.digits),
        digits=int_expansion.digits,
        max_power=int_expansion.max_power - shift,
        sign=sgn(p)
    )


# This is alg:positional_string_to_rational_number in the monograph
def get_fraction(expansion: RadixExpansion) -> Fraction:
    radix = expansion.radix
    l = len(expansion.periodic_digits)

    int_num = sum(d * radix ** (expansion.max_power + expansion.get_shift() - k) for k, d in enumerate(expansion.digits))
    periodic_num = sum(d * radix ** (l - 1 - k) for k, d in enumerate(expansion.periodic_digits))
    periodic_denom = radix ** l - 1

    p = int_num * periodic_denom + periodic_num
    q = periodic_denom * radix ** expansion.get_shift()

    return Fraction(expansion.sign * p, q)
