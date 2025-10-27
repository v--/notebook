from dataclasses import dataclass
from typing import override

from .formulas import ConnectiveFormula, Formula, FormulaVisitor, NegationFormula, QuantifierFormula


@dataclass(frozen=True)
class IsSuperformulaVisitor(FormulaVisitor[bool]):
    subformula: Formula

    @override
    def visit_negation(self, formula: NegationFormula) -> bool:
        return self.visit(formula.body)

    @override
    def visit_connective(self, formula: ConnectiveFormula) -> bool:
        return self.visit(formula.left) or self.visit(formula.right)

    @override
    def visit_quantifier(self, formula: QuantifierFormula) -> bool:
        return self.visit(formula.body)

    @override
    def generic_visit(self, formula: Formula) -> bool:
        return formula == self.subformula


def is_subformula(formula: Formula, subformula: Formula) -> bool:
    return IsSuperformulaVisitor(subformula).visit(formula)
