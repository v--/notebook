from ...parsing import parse_formula
from .axioms import get_induction_axiom
from .signature import ARITHMETIC_SIGNATURE


def test_induction_instance() -> None:
    axiom = get_induction_axiom(parse_formula('(x ≤ Sx)', ARITHMETIC_SIGNATURE))
    expected = parse_formula('(((0 ≤ S0) ∧ ∀y.((y ≤ Sy) → (Sy ≤ SSy))) → ∀y.(y ≤ Sy))', ARITHMETIC_SIGNATURE)
    assert axiom == expected
