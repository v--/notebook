import itertools

from notebook.math.lambda_.common import variables as var
from notebook.math.lambda_.terms import UntypedApplication
from notebook.math.lambda_.terms.terms import UntypedAbstraction
from notebook.math.lambda_.untyped.reduction.api import fully_reduce_term
from notebook.support.coderefs import collector

from .logic import and_, apply_boolean_function, false, iff, implies, is_term_truthy, not_, or_, true


def test_material_implication_reduction() -> None:
    material_implication_equivalence = UntypedAbstraction(
        var.x,
        UntypedAbstraction(
            var.y,
            UntypedApplication(
                UntypedApplication(iff,
                    UntypedApplication(UntypedApplication(or_, UntypedApplication(not_, var.x)), var.y),
                ),
                UntypedApplication(UntypedApplication(implies, var.x), var.y),
            ),
        ),
    )
    for a, b in itertools.product([true, false], repeat=2):
        assert is_term_truthy(
            fully_reduce_term(UntypedApplication(UntypedApplication(material_implication_equivalence, a), b)),
        )


@collector.ref('ex:def:beta_eta_reduction/boolean')
def test_not() -> None:
    for a, in itertools.product([True, False], repeat=1):
        assert apply_boolean_function(not_, a) == (not a)


def test_and() -> None:
    for a, b in itertools.product([True, False], repeat=2):
        assert apply_boolean_function(and_, a, b) == (a and b)


def test_or() -> None:
    for a, b in itertools.product([True, False], repeat=2):
        assert apply_boolean_function(or_, a, b) == (a or b)


def test_implies() -> None:
    for a, b in itertools.product([True, False], repeat=2):
        assert apply_boolean_function(implies, a, b) == (not a or b)


def test_iff() -> None:
    for a, b in itertools.product([True, False], repeat=2):
        assert apply_boolean_function(iff, a, b) == (a == b)
