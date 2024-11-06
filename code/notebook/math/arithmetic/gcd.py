from typing import NamedTuple

from ..matrices.matrix import IntMatrix
from .support import sgn


# This is alg:euclidean_algorithm in the monograph
def gcd(n: int, m: int) -> int:
    while m != 0:
        n, m = m, n % m

    return abs(n)


class ExtendedGcdResult(NamedTuple):
    n: int
    m: int
    a: int
    b: int

    @property
    def gcd(self) -> int:
        return self.a * self.n + self.b * self.m


# This is alg:extended_euclidean_algorithm in the monograph
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
        n, m, sgn(gcd) * a, sgn(gcd) * b
    )
