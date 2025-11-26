import re

import pytest

from ...support.pytest import pytest_parametrize_kwargs
from ..rings.modular import Z2, Z4, Z5, Z7, BaseIntModulo
from .discrete_logarithm import DiscreteLogarithmError, naive_discrete_logarithm


@pytest_parametrize_kwargs(
    dict(base=Z2(1), x=Z2(1), y=0),
    dict(base=Z5(2), x=Z5(2), y=1),
    dict(base=Z5(2), x=Z5(3), y=3),
    dict(base=Z7(3), x=Z7(2), y=2),
    dict(base=Z7(5), x=Z7(3), y=5)
)
def test_naive_discrete_logarithm[T: BaseIntModulo](base: T, x: T, y: int) -> None:
    assert naive_discrete_logarithm(base, x) == y


@pytest_parametrize_kwargs(
    dict(base=Z5(4), x=Z5(3)),
    dict(base=Z7(2), x=Z7(3))
)
def test_naive_discrete_logarithm_failure_nonprime[T: BaseIntModulo](base: T, x: T) -> None:
    with pytest.raises(DiscreteLogarithmError, match=re.escape(f'The base {base!r} is not a primitive root.')):
        naive_discrete_logarithm(base=base, x=x)


def test_naive_discrete_logarithm_failure_composite[T: BaseIntModulo]() -> None:
    with pytest.raises(DiscreteLogarithmError, match='Expected a prime modulus, got 4'):
        naive_discrete_logarithm(base=Z4(2), x=Z4(3))


def test_naive_discrete_logarithm_failure_zero_base[T: BaseIntModulo]() -> None:
    with pytest.raises(DiscreteLogarithmError, match='The base cannot be zero'):
        naive_discrete_logarithm(base=Z5(0), x=Z5(2))


def test_naive_discrete_logarithm_failure_zero_arg[T: BaseIntModulo]() -> None:
    with pytest.raises(DiscreteLogarithmError, match='Zero has no possible logarithms'):
        naive_discrete_logarithm(base=Z5(2), x=Z5(0))
