lazy from collections.abc import Sequence

from notebook.math.lambda_.common import big_omega, combinators, int_to_church_numeral, omega3
from notebook.math.lambda_.common import variables as var
from notebook.math.lambda_.parsing import parse_untyped_term
from notebook.math.lambda_.terms import UntypedApplication, UntypedTerm
from notebook.math.lambda_.untyped.alpha import are_terms_alpha_equivalent
from notebook.support.coderefs import collector
from notebook.support.pytest import pytest_parametrize_kwargs

from .beta import BetaReduction, to_function
from .strategies import ApplicativeOrderStrategy, NormalOrderStrategy, reduce_term_once, transitively_reduce_term


@pytest_parametrize_kwargs(
    dict(term=var.x, expected=None),
    dict(
        term=UntypedApplication(combinators.i, var.x),
        expected=var.x,
    ),
    dict(
        term=parse_untyped_term('((λx.(λy.(xy)))x)'),
        expected=parse_untyped_term('(λy.(xy))'),  # No need to rename
    ),
    dict(
        term=parse_untyped_term('((λx.(λy.(xy)))y)'),
        expected=parse_untyped_term('(λa.(ya))'),  # We rename to avoid capturing
    ),
)
def test_applicative_beta(term: UntypedTerm, expected: UntypedTerm | None) -> None:
    strategy = ApplicativeOrderStrategy(BetaReduction())
    assert strategy.try_reduce(term) == expected


def test_applicative_beta_skk() -> None:
    strategy = ApplicativeOrderStrategy(BetaReduction())
    skk = UntypedApplication(UntypedApplication(combinators.s, combinators.k), combinators.k)

    assert are_terms_alpha_equivalent(
        transitively_reduce_term(skk, strategy),
        combinators.i,
    )


@collector.ref('ex:def:beta_eta_reduction/omega')
def test_applicative_beta_omega() -> None:
    strategy = ApplicativeOrderStrategy(BetaReduction())

    assert reduce_term_once(big_omega, strategy) == big_omega
    assert reduce_term_once(UntypedApplication(omega3, omega3), strategy) == UntypedApplication(UntypedApplication(omega3, omega3), omega3)


@collector.ref('ex:normal_vs_applicative_strategy')
def test_beta_c0_omega_i() -> None:
    applicative = ApplicativeOrderStrategy(BetaReduction())
    normal = NormalOrderStrategy(BetaReduction())

    c0 = int_to_church_numeral(0)
    term = UntypedApplication(UntypedApplication(c0, big_omega), combinators.i)

    assert reduce_term_once(term, applicative) == term
    assert transitively_reduce_term(term, normal) == combinators.i


@pytest_parametrize_kwargs(
    dict(
        term=combinators.i,
        params=[var.x],
        expected=var.x,
    ),
    dict(
        term=combinators.k,
        params=[var.x, var.y],
        expected=var.x,
    ),
    dict(
        term=int_to_church_numeral(0),
        params=[var.x, var.y],
        expected=var.y,
    ),
    dict(
        term=combinators.s,
        params=[var.x, var.y, var.z],
        expected=parse_untyped_term('((xz)(yz))'),
    ),
)
def test_to_function(term: UntypedTerm, params: Sequence[UntypedTerm], expected: UntypedTerm) -> None:
    assert to_function(term)(*params) == expected
