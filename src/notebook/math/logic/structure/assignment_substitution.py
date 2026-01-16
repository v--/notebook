from ..substitution import AtomicLogicSubstitution
from .assignment import VariableAssignment
from .structure import FormalLogicStructure
from .term_visitor import evaluate_term


# This is alg:fol_assignment_substitution in the monograph
def apply_substitution_to_assignment[T](structure: FormalLogicStructure[T], assignment: VariableAssignment[T], substitution: AtomicLogicSubstitution) -> VariableAssignment[T]:
    return VariableAssignment({
        key: evaluate_term(substitution.substitute_variable(key), structure, assignment)
        for key, value in assignment.mapping.items()
    })
