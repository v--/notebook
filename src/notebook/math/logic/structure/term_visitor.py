from dataclasses import dataclass
from typing import override

from ..terms import FunctionApplication, Term, TermVisitor, Variable
from .assignment import VariableAssignment
from .structure import FormalLogicStructure


@dataclass(frozen=True)
class TermEvaluationVisitor[T](TermVisitor[T]):
    structure: FormalLogicStructure
    assignment: VariableAssignment

    @override
    def visit_variable(self, term: Variable) -> T:
        return self.assignment.get_value(term)

    @override
    def visit_function(self, term: FunctionApplication) -> T:
        return self.structure.apply_function(term.symbol, *(self.visit(arg) for arg in term.arguments))


# This is def:fol_denotation/terms in the monograph
def evaluate_term[T](term: Term, structure: FormalLogicStructure[T], assignment: VariableAssignment[T] | None = None) -> T:
    return TermEvaluationVisitor(structure, assignment or VariableAssignment()).visit(term)
