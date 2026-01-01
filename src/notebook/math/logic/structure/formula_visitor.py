from dataclasses import dataclass, field
from typing import override

from ..formulas import (
    ConnectiveFormula,
    EqualityFormula,
    Formula,
    FormulaVisitor,
    NegationFormula,
    PredicateApplication,
    PropConstant,
    QuantifierFormula,
)
from .assignment import VariableAssignment
from .structure import FormalLogicStructure
from .term_visitor import TermEvaluationVisitor


@dataclass
class FormulaEvaluationVisitor[T](FormulaVisitor[bool]):
    structure: FormalLogicStructure
    assignment: VariableAssignment
    term_visitor: TermEvaluationVisitor[T] = field(init=False)

    def __post_init__(self) -> None:
        self.term_visitor = TermEvaluationVisitor(self.structure, self.assignment)

    @override
    def visit_verum(self, formula: PropConstant) -> bool:
        return True

    @override
    def visit_falsum(self, formula: PropConstant) -> bool:
        return False

    @override
    def visit_equality(self, formula: EqualityFormula) -> bool:
        return self.term_visitor.visit(formula.left) == self.term_visitor.visit(formula.right)

    @override
    def visit_predicate(self, formula: PredicateApplication) -> bool:
        return self.structure.apply(formula.symbol, *(self.term_visitor.visit(arg) for arg in formula.arguments))

    @override
    def visit_negation(self, formula: NegationFormula) -> bool:
        return not self.visit(formula.body)

    @override
    def visit_conjunction(self, formula: ConnectiveFormula) -> bool:
        return self.visit(formula.left) and self.visit(formula.right)

    @override
    def visit_disjunction(self, formula: ConnectiveFormula) -> bool:
        return self.visit(formula.left) or self.visit(formula.right)

    @override
    def visit_conditional(self, formula: ConnectiveFormula) -> bool:
        return not self.visit(formula.left) or self.visit(formula.right)

    @override
    def visit_biconditional(self, formula: ConnectiveFormula) -> bool:
        return self.visit(formula.left) == self.visit(formula.right)

    @override
    def visit_universal(self, formula: QuantifierFormula) -> bool:
        return min(
            evaluate_formula(formula.body, self.structure, self.assignment.modify(formula.var, value))
            for value in self.structure.universe
        )

    @override
    def visit_existential(self, formula: QuantifierFormula) -> bool:
        return max(
            evaluate_formula(formula.body, self.structure, self.assignment.modify(formula.var, value))
            for value in self.structure.universe
        )


# This is def:fol_denotation/formulas in the monograph
def evaluate_formula[T](formula: Formula, structure: FormalLogicStructure[T], assignment: VariableAssignment[T] | None = None) -> bool:
    return FormulaEvaluationVisitor(structure, assignment or VariableAssignment()).visit(formula)
