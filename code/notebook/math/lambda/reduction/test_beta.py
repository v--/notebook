from .. import boolean
from .. import combinators as comb
from ..arithmetic import church_numeral, church_numeral_to_int, succ
from ..parsing import parse_term
from ..terms import Application
from ..variables import common as var
from .beta import BetaReduction, to_function
from .strategies import ApplicativeOrderStrategy, NormalOrderStrategy, reduce_term_once, transitively_reduce_term


def test_applicative_beta() -> None:
    strategy = ApplicativeOrderStrategy(BetaReduction())

    assert strategy.try_reduce(var.x) is None
    assert strategy.try_reduce(Application(comb.i, var.x)) == var.x


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


def test_to_function() -> None:
    assert to_function(comb.i)(var.x) == var.x

    assert to_function(boolean.t)(var.x, var.y) == var.x
    assert to_function(boolean.f)(var.x, var.y) == var.y

    assert to_function(comb.s)(var.x, var.y, var.z) == parse_term('((xz)(yz))')
