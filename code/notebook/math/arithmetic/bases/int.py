from dataclasses import dataclass

from ...rings.polynomial.int import IntPolynomial, const, x
from ..divisibility import int_divmod


@dataclass(frozen=True)
class IntRadixExpansion:
    radix: int
    polynomial: IntPolynomial

    def __int__(self) -> int:
        return self.polynomial(x=self.radix)

    def __neg__(self) -> 'IntRadixExpansion':
        return IntRadixExpansion(self.radix, -self.polynomial)

    def __str__(self) -> str:
        return str(int(self))


# This is alg:integer_radix_expansion in the monograph
def get_integer_expansion(n: int, radix: int) -> IntRadixExpansion:
    assert radix >= 2

    if n < radix:
        return IntRadixExpansion(radix, n * const)

    q, r = int_divmod(n, radix)
    pol = get_integer_expansion(q, radix).polynomial
    return IntRadixExpansion(radix, pol * x + r * const)
