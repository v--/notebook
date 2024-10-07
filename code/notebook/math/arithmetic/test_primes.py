import itertools
import random

from ...support.pytest import pytest_parametrize_lists, repeat5
from .primes import are_coprime, factor, is_prime, iter_primes, num_primes, totient


def test_iterate_primes(ceiling: int = 10 ** 3) -> None:
    it = iter(iter_primes(ceiling=ceiling))

    for n in range(1, ceiling):
        if is_prime(n):
            assert n == next(it)


@pytest_parametrize_lists(n=repeat5(random.randint, 1, 100))
def test_num_primes(n: int) -> None:
    assert num_primes(n) == sum(1 for k in iter_primes(ceiling=n))


@pytest_parametrize_lists(n=[-1, 0, 1])
def test_factor_empty(n: int) -> None:
    factorization = factor(n)
    assert len(factorization.multiset) == 0


@pytest_parametrize_lists(
    n=itertools.chain(range(2, 10), repeat5(random.randint, 10, 100))
)
def test_factor(n: int) -> None:
    factorization = factor(n)
    assert int(factorization) == n


@pytest_parametrize_lists(
    n=itertools.chain(range(1, 10), repeat5(random.randint, 10, 100))
)
def test_totient(n: int) -> None:
    assert totient(n) == sum(1 for k in range(1, n + 1) if are_coprime(k, n))
