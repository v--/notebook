from collections.abc import Sequence

from ....support.pytest import pytest_parametrize_kwargs
from .. import boolean
from .. import combinators as comb
from ..arithmetic import church_numeral, church_numeral_to_int, succ
from ..parsing import parse_term
from ..terms import Application, LambdaTerm
from ..variables import common as var
from .beta import BetaReduction, to_function
from .strategies import ApplicativeOrderStrategy, NormalOrderStrategy, reduce_term_once, transitively_reduce_term


@pytest_parametrize_kwargs(
    dict(term=var.x, expected=None),
    dict(
        term=Application(comb.i, var.x),
        expected=var.x
    )
)
def test_applicative_beta(term: LambdaTerm, expected: LambdaTerm | None) -> None:
    strategy = ApplicativeOrderStrategy(BetaReduction())
    assert strategy.try_reduce(term) == expected


def test_applicative_beta_numerals() -> None:
    strategy = ApplicativeOrderStrategy(BetaReduction())

    numeral = church_numeral(0)

    for n in range(10):
        numeral = transitively_reduce_term(Application(succ, numeral), strategy)
        assert church_numeral_to_int(numeral) == n + 1


def test_applicative_beta_omega() -> None:
    strategy = ApplicativeOrderStrategy(BetaReduction())

    assert reduce_term_once(comb.big_omega, strategy) == comb.big_omega
    assert reduce_term_once(Application(comb.omega3, comb.omega3), strategy) == Application(Application(comb.omega3, comb.omega3), comb.omega3)


# ex:normal_vs_applicative_strategy
def test_beta_foi() -> None:
    applicative = ApplicativeOrderStrategy(BetaReduction())
    normal = NormalOrderStrategy(BetaReduction())

    foi = Application(Application(boolean.f, comb.big_omega), comb.i)

    assert reduce_term_once(foi, applicative) == foi
    assert transitively_reduce_term(foi, normal) == comb.i


@pytest_parametrize_kwargs(
    dict(
        term=comb.i,
        params=[var.x],
        expected=var.x
    ),
    dict(
        term=boolean.t,
        params=[var.x, var.y],
        expected=var.x
    ),
    dict(
        term=boolean.f,
        params=[var.x, var.y],
        expected=var.y
    ),
    dict(
        term=comb.s,
        params=[var.x, var.y, var.z],
        expected=parse_term('((xz)(yz))')
    )
)
def test_to_function(term: LambdaTerm, params: Sequence[LambdaTerm], expected: LambdaTerm) -> None:
    assert to_function(term)(*params) == expected
