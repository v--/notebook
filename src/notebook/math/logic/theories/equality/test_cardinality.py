from ....rings.modular import Z3
from ...structure import evaluate_formula
from ..arithmetic import ModularArithmeticStructure
from .cardinality import cardinality_formula_equal, cardinality_formula_geq, cardinality_formula_less


def test_modular_arithmetic_ring() -> None:
    structure = ModularArithmeticStructure(Z3)

    assert evaluate_formula(cardinality_formula_geq(2), structure)
    assert not evaluate_formula(cardinality_formula_geq(4), structure)

    assert evaluate_formula(cardinality_formula_less(4), structure)
    assert not evaluate_formula(cardinality_formula_less(2), structure)

    assert evaluate_formula(cardinality_formula_equal(3), structure)
    assert not evaluate_formula(cardinality_formula_equal(2), structure)
