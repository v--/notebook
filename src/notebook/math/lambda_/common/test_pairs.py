from notebook.math.lambda_.terms import UntypedApplication
from notebook.math.lambda_.untyped.reduction.api import fully_reduce_term
from notebook.support.coderefs import collector

from . import variables as var
from .pairs import car, cdr, cons


@collector.ref('ex:def:beta_eta_reduction/pairs')
def test_applicative_pairs() -> None:
    pair = UntypedApplication(UntypedApplication(cons, var.x), var.y)
    p1 = UntypedApplication(car, pair)
    p2 = UntypedApplication(cdr, pair)

    assert fully_reduce_term(p1)
    assert fully_reduce_term(p2)
