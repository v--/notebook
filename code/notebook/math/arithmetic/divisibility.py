from typing import NamedTuple

from ..linalg.matrix import Matrix
from .support import sgn


# This is eq:rem:integer_division_uniqueness/max/q in the monograph
def quot_max(n: int, m: int) -> int:
    assert m != 0
    # We can't iterate over all integers, so we choose a wide enough range
    domain = range(-abs(n), abs(n) + 1)
    return sgn(m) * max(
        sgn(m) * k for k in domain if k * m <= n
    )


# This is eq:rem:integer_division_uniqueness/trunc/q in the monograph
def quot_trunc(n: int, m: int) -> int:
    assert m != 0
    domain = range(abs(n) + 1)
    return sgn(n) * sgn(m) * max(k for k in domain if k * abs(m) <= abs(n))


# This is eq:rem:integer_division_uniqueness/floor/q in the monograph
def quot_floor(n: int, m: int) -> int:
    assert m != 0
    domain = range(-abs(n), abs(n) + 1)
    return max(k for k in domain if k * abs(m) <= sgn(m) * n)


# This is eq:rem:integer_division_uniqueness/dist/q in the monograph
def quot_dist(n: int, m: int) -> int:
    assert m != 0
    domain = range(-abs(n), abs(n) + 1)
    a, *rest = sorted(domain, key=lambda k: abs(n - k * m))

    if len(rest) > 0:
        b = rest[0]

        if abs(n - a * m) == abs(n - b * m):
            return a if is_even(a) else b

    return a


# This should match quot_max, but is implemented via Python's floor division, which acts like quot_floor
def quot(n: int, m: int, *, raise_if_inexact: bool = False) -> int:
    assert m != 0

    if raise_if_inexact and not divides(m, n):
        raise ValueError(f'{m} does not divide {n}')

    if m > 0:
        return n // m

    return -(-n // m)


def rem(n: int, m: int) -> int:
    return n - m * quot(n, m)


def divides(m: int, n: int) -> bool:
    return rem(n, m) == 0


def is_even(n: int) -> bool:
    return divides(2, n)


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

    state = Matrix([
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
