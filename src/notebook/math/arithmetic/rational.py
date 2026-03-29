from fractions import Fraction

from ...support.coderefs import collector
from .exceptions import InvalidArgumentError


@collector.ref('alg:rational_number_power_bisection')
def power_bisection(x: Fraction, y: Fraction, n: int) -> Fraction:
    if n <= 0:
        raise InvalidArgumentError(f'Expected a positive power, but got {n}')

    if x >= y:
        raise InvalidArgumentError(f'Expected {x} to be less than {y}')

    if x < 1 < y:
        return Fraction(1, 1)

    if x >= 1:
        return 1 / power_bisection(1 / y, 1 / x, n)

    lower = x
    upper = Fraction(1, 1)
    mid = (lower + upper) / 2

    while not x < mid ** n < y:
        if mid ** n <= x:
            lower = mid
        else:
            upper = mid

        mid = (lower + upper) / 2

    return mid
