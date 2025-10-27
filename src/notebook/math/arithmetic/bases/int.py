from dataclasses import dataclass
from typing import NamedTuple

from ...polynomials import monomial
from ...polynomials.polynomial.int import IntPolynomial, const, x
from ..divisibility import int_divmod
from ..support import SignT, sgn


@dataclass(frozen=True)
class IntRadixExpansion:
    radix: int
    polynomial: IntPolynomial
    sign: SignT

    def __getitem__(self, k: int) -> int:
        return self.sign * self.polynomial[monomial.x ** k]

    def __setitem__(self, k: int, value: int) -> None:
        assert 0 <= value < self.radix
        self.polynomial[monomial.x ** k] = value

    def __int__(self) -> int:
        return self.sign * self.polynomial(x=self.radix)

    def __neg__(self) -> IntRadixExpansion:
        return IntRadixExpansion(self.radix, self.polynomial, -self.sign)

    def __abs__(self) -> IntRadixExpansion:
        return IntRadixExpansion(self.radix, self.polynomial, sign=1)

    @property
    def max_power(self) -> int:
        return self.polynomial.total_degree or 0

    def shifted_power(self, k: int) -> IntRadixExpansion:
        pol = IntPolynomial.new_zero()

        for mon in self.polynomial.get_monomials():
            pol[mon * monomial.x ** k] = self.polynomial[mon]

        return IntRadixExpansion(self.radix, pol, self.sign)

    def with_sign(self, sign: SignT) -> IntRadixExpansion:
        return IntRadixExpansion(self.radix, self.polynomial, sign)

    def __str__(self) -> str:
        return str(int(self))


# This is alg:integer_radix_expansion in the monograph
def get_integer_expansion(n: int, radix: int) -> IntRadixExpansion:
    assert radix >= 2

    if abs(n) < radix:
        return IntRadixExpansion(radix, abs(n) * const, sgn(n))

    q, r = int_divmod(abs(n), radix)
    pol = get_integer_expansion(q, radix).polynomial
    return IntRadixExpansion(radix, pol * x + r * const, sgn(n))


# This is alg:addition_with_carrying in the monograph
def add_with_carrying(n: IntRadixExpansion, m: IntRadixExpansion) -> IntRadixExpansion:
    assert n.radix == m.radix

    if n.sign == -1:
        return -add_with_carrying(-n, -m)

    if m.sign == -1 and int(-m) > int(n):
        return -add_with_carrying(-m, -n)

    radix = n.radix
    exp = IntRadixExpansion(radix, IntPolynomial.new_zero(), sign=1)
    q_k = 0
    max_power = max(n.max_power, m.max_power) + 1

    for k in range(max_power + 1):
        sum_ = n[k] + m[k] + q_k
        # This should match q_k, d_k = int_divmod(sum_, radix)
        q_k = 1 if sum_ >= radix else -1 if sum_ < 0 else 0
        d_k = sum_ - q_k * radix
        exp[k] = d_k

    return exp


# This is alg:single_digit_multiplication_with_carrying in the monograph
def single_digit_mult_with_carrying(n: IntRadixExpansion, m: int) -> IntRadixExpansion:
    assert abs(m) < n.radix

    if n.sign == -1 and m < 0:
        return single_digit_mult_with_carrying(-n, -m)

    if n.sign * sgn(m) == -1:
        return -single_digit_mult_with_carrying(abs(n), abs(m))

    radix = n.radix
    exp = IntRadixExpansion(radix, IntPolynomial.new_zero(), sign=1)

    q_k = 0
    max_power = n.max_power + 1

    for k in range(max_power + 1):
        prod = m * n[k] + q_k
        prod_exp = get_integer_expansion(prod, radix)
        q_k = prod_exp[1]
        d_k = prod_exp[0]

        exp[k] = d_k

    return exp


# This is alg:multi_digit_multiplication_with_carrying in the monograph
def multi_digit_mult_with_carrying(n: IntRadixExpansion, m: IntRadixExpansion) -> IntRadixExpansion:
    assert n.radix == m.radix

    radix = n.radix
    exp = IntRadixExpansion(radix, IntPolynomial.new_zero(), sign=1)
    max_power = n.max_power + m.max_power

    for k in range(max_power + 1):
        res = single_digit_mult_with_carrying(n, m[k])
        exp = add_with_carrying(exp, res.shifted_power(k))

    return exp


class ExpansionDivMod(NamedTuple):
    quot: IntRadixExpansion
    rem: IntRadixExpansion


# This is alg:long_integer_division in the monograph
def long_division(n: IntRadixExpansion, m: IntRadixExpansion) -> ExpansionDivMod:
    assert n.radix == m.radix
    assert m.sign != 0
    radix = n.radix

    if n.sign == -1:
        quot, rem = long_division(-n, abs(m))
        quot_ = add_with_carrying(quot, get_integer_expansion(1, radix)).with_sign(-m.sign)
        rem_ = add_with_carrying(abs(m), -rem)
        return ExpansionDivMod(quot_, rem_)

    if m.sign == -1:
        quot, rem = long_division(n, -m)
        return ExpansionDivMod(-quot, rem)

    rem = n
    quot = IntRadixExpansion(radix, IntPolynomial.new_zero(), sign=1)

    for s in range(n.max_power - m.max_power + 1):
        k = n.max_power - m.max_power - s
        m_ = m.shifted_power(k)
        q_k = max(q for q in range(radix) if q * int(m_) <= int(rem))
        quot[k] = q_k

        rem = add_with_carrying(
            rem,
            -single_digit_mult_with_carrying(m_, q_k)
        )

    return ExpansionDivMod(quot, rem)
