from dataclasses import dataclass
from typing import override

from ..alphabet import BinaryConnective, PropConstant
from ..formulas import (
    ConnectiveFormula,
    ConstantFormula,
    Formula,
    NegationFormula,
)
from .formula_visitor import PropositionalFormulaVisitor
from .interpretation import PropositionalInterpretation
from .variables import PropositionalVariableFormula, extract_variable


@dataclass
class FormulaEvaluationVisitor[T](PropositionalFormulaVisitor[bool]):
    interpretation: PropositionalInterpretation

    @override
    def visit_logical_constant(self, formula: ConstantFormula) -> bool:
        match formula.value:
            case PropConstant.VERUM:
                return True

            case PropConstant.FALSUM:
                return False

    @override
    def visit_propositional_variable(self, formula: PropositionalVariableFormula) -> bool:
        return self.interpretation.get_value(extract_variable(formula))

    @override
    def visit_negation(self, formula: NegationFormula) -> bool:
        return not self.visit(formula.body)

    @override
    def visit_connective(self, formula: ConnectiveFormula) -> bool:
        match formula.conn:
            case BinaryConnective.CONJUNCTION:
                return self.visit(formula.left) and self.visit(formula.right)

            case BinaryConnective.DISJUNCTION:
                return self.visit(formula.left) or self.visit(formula.right)

            case BinaryConnective.CONDITIONAL:
                return not self.visit(formula.left) or self.visit(formula.right)

            case BinaryConnective.BICONDITIONAL:
                return self.visit(formula.left) == self.visit(formula.right)


# This is def:propositional_denotation in the monograph
def evaluate_propositional_formula(formula: Formula, interpretation: PropositionalInterpretation) -> bool:
    return FormulaEvaluationVisitor(interpretation).visit(formula)
