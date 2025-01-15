from collections.abc import Sequence

from .....support.pytest import pytest_parametrize_kwargs
from ...common import big_omega, church_numeral, church_numeral_to_int, combinators, omega3, pairs, succ
from ...common import variables as var
from ...parsing import parse_pure_term
from ...terms import Application, LambdaTerm
from ..alpha import are_terms_alpha_equivalent
from .beta import BetaReduction, to_function
from .strategies import ApplicativeOrderStrategy, NormalOrderStrategy, reduce_term_once, transitively_reduce_term


@pytest_parametrize_kwargs(
    dict(term=var.x, expected=None),
    dict(
        term=Application(combinators.i, var.x),
        expected=var.x
    ),
    dict(
        term=parse_pure_term('((λx.(λy.(xy)))x)'),
        expected=parse_pure_term('(λy.(xy))') # We avoid renaming
    ),
    dict(
        term=parse_pure_term('((λx.(λy.(xy)))y)'),
        expected=parse_pure_term('(λa.(ya))') # We rename to avoid capturing
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


def test_applicative_beta_skk() -> None:
    strategy = ApplicativeOrderStrategy(BetaReduction())
    skk = Application(Application(combinators.s, combinators.k), combinators.k)

    assert are_terms_alpha_equivalent(
        transitively_reduce_term(skk, strategy),
        combinators.i
    )


def test_applicative_beta_omega() -> None:
    strategy = ApplicativeOrderStrategy(BetaReduction())

    assert reduce_term_once(big_omega, strategy) == big_omega
    assert reduce_term_once(Application(omega3, omega3), strategy) == Application(Application(omega3, omega3), omega3)


# ex:normal_vs_applicative_strategy
def test_beta_cdr_omega_i() -> None:
    applicative = ApplicativeOrderStrategy(BetaReduction())
    normal = NormalOrderStrategy(BetaReduction())

    foi = Application(Application(pairs.cdr, big_omega), combinators.i)

    assert reduce_term_once(foi, applicative) == foi
    assert transitively_reduce_term(foi, normal) == combinators.i


@pytest_parametrize_kwargs(
    dict(
        term=combinators.i,
        params=[var.x],
        expected=var.x
    ),
    dict(
        term=pairs.car,
        params=[var.x, var.y],
        expected=var.x
    ),
    dict(
        term=pairs.cdr,
        params=[var.x, var.y],
        expected=var.y
    ),
    dict(
        term=combinators.s,
        params=[var.x, var.y, var.z],
        expected=parse_pure_term('((xz)(yz))')
    )
)
def test_to_function(term: LambdaTerm, params: Sequence[LambdaTerm], expected: LambdaTerm) -> None:
    assert to_function(term)(*params) == expected
