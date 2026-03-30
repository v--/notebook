import math

from ...support.coderefs import collector
from .exceptions import InvalidArgumentError


@collector.ref('eq:thm:stirlings_gamma_approximation/mu')
def stirling_mu(x: float, terms: int) -> float:
    return sum(
        (x + k + 1 / 2) * math.log(1 + 1 / (x + k)) - 1
        for k in range(terms)
    )


@collector.ref('thm:stirlings_gamma_approximation')
def stirling(x: float) -> float:
    if x <= 0:
        raise InvalidArgumentError(f'Expected a positive number, but got {x:.3f}')

    return math.sqrt(2 * math.pi) * x ** (x - 1 / 2) * math.exp(-x)
