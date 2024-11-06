from .support import sgn
from typing import NamedTuple


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


class DivMod(NamedTuple):
    quot: int
    rem: int


def divmod(n: int, m: int) -> DivMod:
    q = quot(n, m)
    return DivMod(q, n - m * q)


def divides(m: int, n: int) -> bool:
    return rem(n, m) == 0


def is_even(n: int) -> bool:
    return divides(2, n)
