from dataclasses import dataclass
from typing import override

from ..formulas import PropConstant
from .formula_visitor import PropFormulaVisitor
from .formulas import (
    PropConnectiveFormula,
    PropFormula,
    PropNegationFormula,
    PropVariable,
)
from .interpretation import PropInterpretation


@dataclass
class FormulaEvaluationVisitor[T](PropFormulaVisitor[bool]):
    interpretation: PropInterpretation

    @override
    def visit_verum(self, formula: PropConstant) -> bool:
        return True

    @override
    def visit_falsum(self, formula: PropConstant) -> bool:
        return False

    @override
    def visit_variable(self, formula: PropVariable) -> bool:
        return self.interpretation.get_value(formula)

    @override
    def visit_negation(self, formula: PropNegationFormula) -> bool:
        return not self.visit(formula.body)

    @override
    def visit_conjunction(self, formula: PropConnectiveFormula) -> bool:
        return self.visit(formula.left) and self.visit(formula.right)

    @override
    def visit_disjunction(self, formula: PropConnectiveFormula) -> bool:
        return self.visit(formula.left) or self.visit(formula.right)

    @override
    def visit_conditional(self, formula: PropConnectiveFormula) -> bool:
        return not self.visit(formula.left) or self.visit(formula.right)

    @override
    def visit_biconditional(self, formula: PropConnectiveFormula) -> bool:
        return self.visit(formula.left) == self.visit(formula.right)


# This is alg:propositional_denotation in the monograph
def evaluate_prop_formula(formula: PropFormula, interpretation: PropInterpretation) -> bool:
    return FormulaEvaluationVisitor(interpretation).visit(formula)
