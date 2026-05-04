from dataclasses import dataclass
from typing import TYPE_CHECKING, override

from notebook.math.logic.terms import FunctionApplication, Term, TermVisitor, Variable
from notebook.support.coderefs import collector

from .assignment import VariableAssignment


if TYPE_CHECKING:
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
        return self.structure.apply(term.symbol, *(self.visit(arg) for arg in term.arguments))


@collector.ref('alg:fol_term_denotation')
def evaluate_term[T](term: Term, structure: FormalLogicStructure[T], assignment: VariableAssignment[T] | None = None) -> T:
    return TermEvaluationVisitor(structure, assignment or VariableAssignment()).visit(term)
