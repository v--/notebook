import itertools
from dataclasses import dataclass

from ...polynomials import monomial
from ...polynomials.polynomial.int import IntPolynomial, const, x
from ..divisibility import int_divmod
from ..support import sgn


@dataclass(frozen=True)
class IntRadixExpansion:
    radix: int
    polynomial: IntPolynomial

    def __int__(self) -> int:
        return self.polynomial(x=self.radix)

    def __str__(self) -> str:
        return str(int(self))


# This is alg:nonnegative_integer_radix_expansion in the monograph
def get_integer_expansion(n: int, radix: int) -> IntRadixExpansion:
    assert radix >= 2
    assert n >= 0

    if n < radix:
        return IntRadixExpansion(radix, n * const)

    q, r = int_divmod(n, radix)
    pol = get_integer_expansion(q, radix).polynomial
    return IntRadixExpansion(radix, pol * x + r * const)


# This is alg:addition_with_carrying in the monograph
def add_with_carrying(n: int, m: int, radix: int) -> int:
    if n < 0:
        return -add_with_carrying(-n, -m, radix)

    if m < 0 and -m > n:
        return -add_with_carrying(-m, -n, radix)

    pol_n = get_integer_expansion(n, radix).polynomial
    pol_m = get_integer_expansion(abs(m), radix).polynomial
    pol = 0 * const

    q_k = 0
    max_power = max(pol_n.total_degree or 0, pol_m.total_degree or 0) + 1

    for k in range(max_power + 1):
        mon = monomial.x ** k
        a_k = pol_n[mon]
        c_k = pol_m[mon]

        q_k, d_k = int_divmod(a_k + sgn(m) * c_k + q_k, radix)
        pol[mon] = d_k

    return pol(x=radix)
