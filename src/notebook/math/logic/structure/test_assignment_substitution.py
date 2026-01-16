from ...rings.modular import Z5
from ..parsing import parse_term, parse_variable
from ..substitution import AtomicLogicSubstitution, apply_substitution_to_term
from ..theories.arithmetic import ARITHMETIC_SIGNATURE, ModularArithmeticStructure
from .assignment import VariableAssignment
from .assignment_substitution import apply_substitution_to_assignment
from .term_visitor import evaluate_term


def test_apply_substitution_to_assignment() -> None:
    term = parse_term('(x + y)', ARITHMETIC_SIGNATURE)
    structure = ModularArithmeticStructure(Z5)

    substitution = AtomicLogicSubstitution(
        variable_mapping={
            parse_variable('x'): parse_term('Sy', ARITHMETIC_SIGNATURE),
            parse_variable('y'): parse_term('Sx', ARITHMETIC_SIGNATURE)
        }
    )
    subst_term = apply_substitution_to_term(term, substitution)

    assignment = VariableAssignment.infer(x=Z5(2), y=Z5(1))
    subst_assignment = apply_substitution_to_assignment(structure, assignment, substitution)

    assert evaluate_term(subst_term, structure, assignment) == evaluate_term(term, structure, subst_assignment)

