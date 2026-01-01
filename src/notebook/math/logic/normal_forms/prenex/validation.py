from typing import override

from ...formulas import (
    ConnectiveFormula,
    Formula,
    FormulaVisitor,
    NegationFormula,
    QuantifierFormula,
)


class PNFValidationVisitor(FormulaVisitor[bool]):
    @override
    def visit_atomic(self, formula: Formula) -> bool:
        return True

    @override
    def visit_negation(self, formula: NegationFormula) -> bool:
        if isinstance(formula.body, QuantifierFormula):
            return False

        return self.visit(formula.body)

    @override
    def visit_connective(self, formula: ConnectiveFormula) -> bool:
        if isinstance(formula.left, QuantifierFormula) or isinstance(formula.right, QuantifierFormula):
            return False

        return self.visit(formula.left) and self.visit(formula.right)

    @override
    def visit_quantifier(self, formula: QuantifierFormula) -> bool:
        return self.visit(formula.body)


def is_formula_in_pnf(formula: Formula) -> bool:
    return PNFValidationVisitor().visit(formula)
