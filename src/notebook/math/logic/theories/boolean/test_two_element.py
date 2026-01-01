from ...structure import evaluate_formula
from .axioms import BOOLEAN_ALGEBRA_AXIOMS
from .two_element import TwoElementBooleanAlgebra


def test_power_set_algebra_axioms() -> None:
    structure = TwoElementBooleanAlgebra()

    for axiom in BOOLEAN_ALGEBRA_AXIOMS:
        assert evaluate_formula(axiom, structure)
