import itertools
import math
from collections import Counter
from collections.abc import Iterable, Sequence
from dataclasses import dataclass

from .divisibility import divides, quot
from .gcd import gcd
from .support import SignT, sgn


def build_erathostenes_sieve(ceiling: int) -> Sequence[bool]:
    assert ceiling > 0
    ceil_sqrt = math.isqrt(ceiling)

    sieve = [True] * (ceiling + 1)
    sieve[0] = sieve[1] = False

    for k in range(2, ceil_sqrt + 1):
        if not sieve[k]:
            continue

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


def is_prime_naive(n: int) -> bool:
    assert n > 0

    if n == 1:
        return False

    return all(
        not divides(k, n) for k in range(2, math.isqrt(n) + 1)
    )


def num_primes(n: int) -> int:
    assert n > 0
    return sum(build_erathostenes_sieve(ceiling=n))


# thm:inclusion_exclusion_eratosthenes
def num_primes_inclusion_exclusion(n: int) -> int:
    assert n > 0
    p = list(iter_primes(math.isqrt(n)))
    result = (n - 1) + len(p)

    for m in range(1, len(p) + 1):
        for c in itertools.combinations(p, m):
            result += (-1) ** len(c) * (n // math.prod(c))

    return result


@dataclass(frozen=True)
class PrimeFactorization:
    multiset: Counter[int]
    sign: SignT

    def __int__(self) -> int:
        if self.multiset.total() == 0:
            return 0

        return self.sign * math.prod(p ** k for p, k in self.multiset.items())

    def __and__(self, other: PrimeFactorization) -> PrimeFactorization:
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
