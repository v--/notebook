import itertools
import math
from collections import Counter
from collections.abc import Iterable, Sequence
from typing import NamedTuple

from .divisibility import divides, gcd, quot
from .support import SignT, sgn


def build_erathostenes_sieve(ceiling: int) -> Sequence[bool]:
    assert ceiling > 0

    sieve = [True] * (ceiling + 1)
    sieve[0] = sieve[1] = False

    for k in range(2, ceiling + 1):
        for m in itertools.count(2):
            if k * m > ceiling:
                break

            sieve[k * m] = False

    return sieve


def iter_primes(ceiling: int) -> Iterable[int]:
    assert ceiling > 0
    sieve = build_erathostenes_sieve(ceiling)

    for k in range(2, ceiling + 1):
        if sieve[k]:
            yield k


def is_prime(n: int) -> bool:
    assert n > 0

    if n == 1:
        return False

    return all(
        divides(n, k) for k in range(2, math.isqrt(n) + 1)
    )


def num_primes(n: int) -> int:
    assert n > 0
    return sum(build_erathostenes_sieve(ceiling=n))


class PrimeFactorization(NamedTuple):
    multiset: Counter[int]
    sign: SignT

    def __int__(self) -> int:
        if self.multiset.total() == 0:
            return 0

        return self.sign * math.prod(p ** k for p, k in self.multiset.items())

    def __and__(self, other: 'PrimeFactorization') -> 'PrimeFactorization':
        return PrimeFactorization(
            multiset=self.multiset & other.multiset,
            sign=sgn(self.sign * other.sign)
        )


def factor(n: int) -> PrimeFactorization:
    multiset: Counter[int] = Counter()
    r = abs(n)

    for p in range(2, r // 2 + 1):
        while divides(p, r):
            multiset[p] += 1
            r = quot(r, p)

        if r <= 1:
            break

    # Prime number
    if r > 1 and len(multiset) == 0:
        multiset[r] = 1

    return PrimeFactorization(
        multiset=multiset,
        sign=sgn(n)
    )


def are_coprime(n: int, m: int) -> bool:
    return gcd(n, m) == 1


def build_coprimality_sieve(n: int) -> Sequence[bool]:
    assert n > 0

    factorization = factor(n)
    sieve = [True] * (n + 1)
    sieve[0] = False

    for p in factorization.multiset.elements():
        for m in itertools.count(1):
            if m * p > n:
                break

            sieve[m * p] = False

    return sieve


def totient(n: int) -> int:
    assert n > 0
    return sum(build_coprimality_sieve(n))
