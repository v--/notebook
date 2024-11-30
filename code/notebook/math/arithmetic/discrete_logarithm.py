from ...exceptions import UnreachableException
from ..rings.modulo import BaseIntModulo
from .exceptions import NotebookArithmeticError
from .primes import are_coprime, is_prime_naive


class DiscreteLogarithmError(NotebookArithmeticError):
    pass


def naive_discrete_logarithm[T: BaseIntModulo](base: T, x: T) -> int:
    """Find a nonnegative integer y such that bʸ = x (mod p)"""

    if not is_prime_naive(base.modulus):
        raise DiscreteLogarithmError(f'Expected a prime modulus, got {base.modulus!r}')

    if int(base) == 0:
        raise DiscreteLogarithmError('The base cannot be zero')

    if int(x) == 0:
        raise DiscreteLogarithmError('Zero has no possible logarithms')

    for y in range(base.modulus):
        if base ** y == x:
            return y

    raise DiscreteLogarithmError(f'The base {base!r} is not a primitive root.')
