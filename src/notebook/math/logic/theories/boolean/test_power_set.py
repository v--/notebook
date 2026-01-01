from ...structure import evaluate_formula
from .axioms import BOOLEAN_ALGEBRA_AXIOMS
from .power_set import PowerSetBooleanAlgebra


def test_power_set_algebra_axioms(n: int = 3) -> None:
    structure = PowerSetBooleanAlgebra(set(range(n)))

    for axiom in BOOLEAN_ALGEBRA_AXIOMS:
        assert evaluate_formula(axiom, structure)
