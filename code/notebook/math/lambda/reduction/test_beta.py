from .. import boolean
from .. import combinators as comb
from ..arithmetic import church_numeral, church_numeral_to_int, succ
from ..parsing import parse_term
from ..terms import Application
from ..variables import common as var
from .beta import BetaReduction, to_function
from .strategies import NormalOrderStrategy, transitively_reduce_term


def test_applicative_beta() -> None:
    strategy = NormalOrderStrategy(BetaReduction())

    assert strategy.try_reduce(var.x) is None
    assert strategy.try_reduce(Application(comb.i, var.x)) == var.x


def test_applicative_beta_numerals() -> None:
    strategy = NormalOrderStrategy(BetaReduction())

    numeral = church_numeral(0)

    for n in range(10):
        numeral = transitively_reduce_term(Application(succ, numeral), strategy)
        assert church_numeral_to_int(numeral) == n + 1


def test_to_function() -> None:
    assert to_function(comb.i)(var.x) == var.x

    assert to_function(boolean.t)(var.x, var.y) == var.x
    assert to_function(boolean.f)(var.x, var.y) == var.y

    assert to_function(comb.s)(var.x, var.y, var.z) == parse_term('((xz)(yz))')
