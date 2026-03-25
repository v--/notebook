from typing import TYPE_CHECKING

from .assignment import VariableAssignment
from .term_visitor import evaluate_term


if TYPE_CHECKING:
    from ..substitution import AtomicLogicSubstitution
    from .structure import FormalLogicStructure


# This is alg:fol_assignment_substitution in the monograph
def apply_substitution_to_assignment[T](structure: FormalLogicStructure[T], assignment: VariableAssignment[T], substitution: AtomicLogicSubstitution) -> VariableAssignment[T]:
    return VariableAssignment({
        key: evaluate_term(substitution.substitute_variable(key), structure, assignment)
        for key in assignment.mapping
    })
