from collections.abc import Sequence

from .....support.pytest import pytest_parametrize_kwargs
from ...common import big_omega, church_numeral, church_numeral_to_int, combinators, omega3, pairs, succ
from ...common import variables as var
from ...parsing import parse_pure_term
from ...terms import UntypedAbstraction, UntypedApplication, UntypedTerm
from ..alpha import are_terms_alpha_equivalent
from .beta import BetaReduction, to_function
from .strategies import ApplicativeOrderStrategy, NormalOrderStrategy, reduce_term_once, transitively_reduce_term


@pytest_parametrize_kwargs(
    dict(term=var.x, expected=None),
    dict(
        term=UntypedApplication(combinators.i, var.x),
        expected=var.x
    ),
    dict(
        term=parse_pure_term('((λx.(λy.(xy)))x)'),
        expected=parse_pure_term('(λy.(xy))')  # No need to rename
    ),
    dict(
        term=parse_pure_term('((λx.(λy.(xy)))y)'),
        expected=parse_pure_term('(λa.(ya))')  # We rename to avoid capturing
    )
)
def test_applicative_beta(term: UntypedTerm, expected: UntypedTerm | None) -> None:
    strategy = ApplicativeOrderStrategy(BetaReduction())
    assert strategy.try_reduce(term) == expected


def test_applicative_beta_numerals() -> None:
    strategy = ApplicativeOrderStrategy(BetaReduction())

    numeral = church_numeral(0)

    for n in range(10):
        numeral = transitively_reduce_term(UntypedApplication(succ, numeral), strategy)
        assert church_numeral_to_int(numeral) == n + 1


def test_applicative_beta_skk() -> None:
    strategy = ApplicativeOrderStrategy(BetaReduction())
    skk = UntypedApplication(UntypedApplication(combinators.s, combinators.k), combinators.k)

    assert are_terms_alpha_equivalent(
        transitively_reduce_term(skk, strategy),
        combinators.i
    )


# ex:def:beta_eta_reduction/omega
def test_applicative_beta_omega() -> None:
    strategy = ApplicativeOrderStrategy(BetaReduction())

    assert reduce_term_once(big_omega, strategy) == big_omega
    assert reduce_term_once(UntypedApplication(omega3, omega3), strategy) == UntypedApplication(UntypedApplication(omega3, omega3), omega3)


# ex:def:beta_eta_reduction/pairs
def test_applicative_pairs() -> None:
    strategy = ApplicativeOrderStrategy(BetaReduction())

    pair = UntypedApplication(UntypedApplication(pairs.cons, var.x), var.y)
    p1 = UntypedApplication(pairs.car, pair)
    p2 = UntypedApplication(pairs.cdr, pair)

    assert transitively_reduce_term(p1, strategy) == var.x
    assert transitively_reduce_term(p2, strategy) == var.y


# ex:def:beta_eta_reduction/boolean
def test_applicative_not() -> None:
    strategy = ApplicativeOrderStrategy(BetaReduction())

    t = combinators.k
    f = church_numeral(0)
    n = UntypedAbstraction(var.x, UntypedApplication(UntypedApplication(var.x, f), t))

    assert transitively_reduce_term(UntypedApplication(n, t), strategy) == f
    assert transitively_reduce_term(UntypedApplication(n, f), strategy) == t


# ex:normal_vs_applicative_strategy
def test_beta_c0_omega_i() -> None:
    applicative = ApplicativeOrderStrategy(BetaReduction())
    normal = NormalOrderStrategy(BetaReduction())

    c0 = church_numeral(0)
    term = UntypedApplication(UntypedApplication(c0, big_omega), combinators.i)

    assert reduce_term_once(term, applicative) == term
    assert transitively_reduce_term(term, normal) == combinators.i


@pytest_parametrize_kwargs(
    dict(
        term=combinators.i,
        params=[var.x],
        expected=var.x
    ),
    dict(
        term=combinators.k,
        params=[var.x, var.y],
        expected=var.x
    ),
    dict(
        term=church_numeral(0),
        params=[var.x, var.y],
        expected=var.y
    ),
    dict(
        term=combinators.s,
        params=[var.x, var.y, var.z],
        expected=parse_pure_term('((xz)(yz))')
    )
)
def test_to_function(term: UntypedTerm, params: Sequence[UntypedTerm], expected: UntypedTerm) -> None:
    assert to_function(term)(*params) == expected
