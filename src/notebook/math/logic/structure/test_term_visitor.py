from ...rings.modular import Z2
from ..parsing import parse_term
from ..theories.arithmetic import ARITHMETIC_SIGNATURE, ModularArithmeticStructure
from .assignment import VariableAssignment
from .term_visitor import evaluate_term


def test_addition_with_constants() -> None:
    term = parse_term('(0 + 0)', ARITHMETIC_SIGNATURE)
    structure = ModularArithmeticStructure(Z2)
    assert evaluate_term(term, structure) == Z2(0)


def test_addition_with_variables() -> None:
    term = parse_term('(x + y)', ARITHMETIC_SIGNATURE)
    structure = ModularArithmeticStructure(Z2)
    assignment = VariableAssignment.infer(x=Z2(1), y=Z2(1))
    assert evaluate_term(term, structure, assignment) == Z2(0)
