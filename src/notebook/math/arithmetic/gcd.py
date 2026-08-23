from collections.abc import Sequence
from dataclasses import dataclass

from notebook.math.matrices.matrix import IntMatrix
from notebook.support.coderefs import collector

from .divisibility import rem
from .exceptions import InvalidArgumentError, NotCoprimeError
from .support import sgn


@collector.ref('alg:euclidean_algorithm')
def gcd(n: int, m: int) -> int:
    while m != 0:
        n, m = m, n % m

    return abs(n)


@dataclass(frozen=True)
class ExtendedGcdResult:
    n: int
    m: int
    a: int
    b: int

    @property
    def gcd(self) -> int:
        return self.a * self.n + self.b * self.m


@collector.ref('alg:extended_euclidean_algorithm')
def extended_gcd(n: int, m: int) -> ExtendedGcdResult:
    i_r = 0
    i_a = 1
    i_b = 2

    state = IntMatrix.from_rows([
        [n, m],  # r
        [1, 0],  # a
        [0, 1],  # b
    ])

    while state[i_r, 1] != 0:
        q = state[i_r, 0] // state[i_r, 1]

        new_col = state[:, 0] - q * state[:, 1]
        state[:, 0] = state[:, 1]
        state[:, 1] = new_col

    a = state[i_a, 0]
    b = state[i_b, 0]
    gcd = a * n + b * m

    return ExtendedGcdResult(
        n, m, sgn(gcd) * a, sgn(gcd) * b,
    )


@dataclass(frozen=True)
class ModularEquation:
    value: int
    modulus: int


@collector.ref('alg:chinese_remainder_theorem_iteration')
def chinese_remainder_theorem_iteration(equations: Sequence[ModularEquation]) -> int:
    if len(equations) == 0:
        raise InvalidArgumentError('No equations given')

    if len(equations) == 1:
        eq = equations[0]
        return rem(eq.value, eq.modulus)

    *rest, eq_pen, eq_last = equations
    egcd = extended_gcd(eq_pen.modulus, eq_last.modulus)

    if egcd.a * eq_pen.modulus + egcd.b * eq_last.modulus != 1:
        raise NotCoprimeError(eq_pen.modulus, eq_last.modulus)

    x = egcd.a * eq_pen.modulus * eq_last.value + egcd.b * eq_last.modulus * eq_pen.value
    return chinese_remainder_theorem_iteration(
        [*rest, ModularEquation(x, eq_pen.modulus * eq_last.modulus)],
    )
