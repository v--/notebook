from dataclasses import dataclass
from typing import NamedTuple

from notebook.math.arithmetic.divisibility import int_divmod
from notebook.math.arithmetic.exceptions import InvalidArgumentError, NotebookZeroDivisionError, RadixError
from notebook.math.arithmetic.support import SignT, sgn
from notebook.math.polynomials import monomial
from notebook.math.polynomials.polynomial.int import IntPolynomial, const, x
from notebook.parsing import common_identifiers as ci
from notebook.support.coderefs import collector


@dataclass(frozen=True)
class IntRadixExpansion:
    radix: int
    polynomial: IntPolynomial
    sign: SignT

    def __getitem__(self, k: int) -> int:
        return self.sign * self.polynomial[monomial.x ** k]

    def __setitem__(self, k: int, value: int) -> None:
        if value < 0 or value >= self.radix:
            raise InvalidArgumentError(f'Expected a nonnegative integer less than {self.radix}, but got {value}')

        self.polynomial[monomial.x ** k] = value

    def __int__(self) -> int:
        return self.sign * self.polynomial(x=self.radix)

    def __neg__(self) -> IntRadixExpansion:
        return IntRadixExpansion(self.radix, self.polynomial, -self.sign)

    def __abs__(self) -> IntRadixExpansion:
        return IntRadixExpansion(self.radix, self.polynomial, sign=1)

    @property
    def max_power(self) -> int:
        return self.polynomial.get_max_power(ci.x)

    def shifted_power(self, k: int) -> IntRadixExpansion:
        pol = IntPolynomial.new_zero()

        for mon in self.polynomial.get_monomials():
            pol[mon * monomial.x ** k] = self.polynomial[mon]

        return IntRadixExpansion(self.radix, pol, self.sign)

    def with_sign(self, sign: SignT) -> IntRadixExpansion:
        return IntRadixExpansion(self.radix, self.polynomial, sign)

    def __str__(self) -> str:
        return str(int(self))


@collector.ref('alg:integer_radix_expansion')
def get_integer_expansion(n: int, radix: int) -> IntRadixExpansion:
    if radix < 2:
        raise RadixError(f'Invalid radix {radix}')

    if abs(n) < radix:
        return IntRadixExpansion(radix, abs(n) * const, sgn(n))

    q, r = int_divmod(abs(n), radix)
    pol = get_integer_expansion(q, radix).polynomial
    return IntRadixExpansion(radix, pol * x + r * const, sgn(n))


@collector.ref('alg:addition_with_carrying')
def add_with_carrying(n: IntRadixExpansion, m: IntRadixExpansion) -> IntRadixExpansion:
    if n.radix != m.radix:
        raise RadixError(f'Incompatible radixes {n.radix} and {m.radix}')

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


@collector.ref('alg:single_digit_multiplication_with_carrying')
def single_digit_mult_with_carrying(n: IntRadixExpansion, m: int) -> IntRadixExpansion:
    if abs(m) >= n.radix:
        raise InvalidArgumentError(f'Expected an integer with absolute value less than {n.radix}, but got {m}')

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


@collector.ref('alg:multi_digit_multiplication_with_carrying')
def multi_digit_mult_with_carrying(n: IntRadixExpansion, m: IntRadixExpansion) -> IntRadixExpansion:
    if n.radix != m.radix:
        raise RadixError(f'Incompatible radixes {n.radix} and {m.radix}')

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


@collector.ref('alg:long_integer_division')
def long_division(n: IntRadixExpansion, m: IntRadixExpansion) -> ExpansionDivMod:
    if n.radix != m.radix:
        raise RadixError(f'Incompatible radixes {n.radix} and {m.radix}')

    if m.sign == 0:
        raise NotebookZeroDivisionError(int(m))

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
            -single_digit_mult_with_carrying(m_, q_k),
        )

    return ExpansionDivMod(quot, rem)
