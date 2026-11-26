from notebook.math.lambda_.common import variables as var
from notebook.math.lambda_.parsing import parse_untyped_term
from notebook.math.lambda_.untyped.reduction.eta import EtaReduction
from notebook.support.pytest import pytest_parametrize_kwargs
lazy from notebook.math.lambda_.terms import UntypedTerm

from .strategies import ApplicativeOrderStrategy


@pytest_parametrize_kwargs(
    dict(term=var.x, expected=None),
    dict(
        term=parse_untyped_term('(λx.((λy.y)x))'),
        expected=parse_untyped_term('(λy.y)'),
    ),
    dict(
        term=parse_untyped_term('(λx.((λy.x)x))'),
        expected=None,
    ),
)
def test_applicative_eta(term: UntypedTerm, expected: UntypedTerm | None) -> None:
    strategy = ApplicativeOrderStrategy(EtaReduction())
    assert strategy.try_reduce(term) == expected
