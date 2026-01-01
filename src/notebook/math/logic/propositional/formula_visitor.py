from typing import override

from ..alphabet import BinaryConnective, PropConstantSymbol
from ..formulas import PropConstant
from .formulas import (
    PropConnectiveFormula,
    PropFormula,
    PropNegationFormula,
    PropVariable,
)


class PropFormulaVisitor[T]:
    def visit(self, formula: PropFormula) -> T:
        match formula:
            case PropConstant():
                match formula.value:
                    case PropConstantSymbol.VERUM:
                        return self.visit_verum(formula)

                    case PropConstantSymbol.FALSUM:
                        return self.visit_falsum(formula)

            case PropVariable():
                return self.visit_variable(formula)

            case PropNegationFormula():
                return self.visit_negation(formula)

            case PropConnectiveFormula():
                match formula.conn:
                    case BinaryConnective.CONJUNCTION:
                        return self.visit_conjunction(formula)

                    case BinaryConnective.DISJUNCTION:
                        return self.visit_disjunction(formula)

                    case BinaryConnective.CONDITIONAL:
                        return self.visit_conditional(formula)

                    case BinaryConnective.BICONDITIONAL:
                        return self.visit_biconditional(formula)

    def visit_atomic(self, formula: PropConstant | PropVariable) -> T:
        return self.generic_visit(formula)

    def visit_prop_constant(self, formula: PropConstant) -> T:
        return self.visit_atomic(formula)

    def visit_verum(self, formula: PropConstant) -> T:
        return self.visit_prop_constant(formula)

    def visit_falsum(self, formula: PropConstant) -> T:
        return self.visit_prop_constant(formula)

    def visit_variable(self, formula: PropVariable) -> T:
        return self.visit_atomic(formula)

    def visit_negation(self, formula: PropNegationFormula) -> T:
        return self.generic_visit(formula)

    def visit_connective(self, formula: PropConnectiveFormula) -> T:
        return self.generic_visit(formula)

    def visit_conjunction(self, formula: PropConnectiveFormula) -> T:
        return self.visit_connective(formula)

    def visit_disjunction(self, formula: PropConnectiveFormula) -> T:
        return self.visit_connective(formula)

    def visit_conditional(self, formula: PropConnectiveFormula) -> T:
        return self.visit_connective(formula)

    def visit_biconditional(self, formula: PropConnectiveFormula) -> T:
        return self.visit_connective(formula)

    def generic_visit(self, formula: PropFormula) -> T:
        raise NotImplementedError


class PropFormulaTransformationVisitor(PropFormulaVisitor[PropFormula]):
    @override
    def visit_atomic(self, formula: PropConstant | PropVariable) -> PropFormula:
        return formula

    @override
    def visit_negation(self, formula: PropNegationFormula) -> PropFormula:
        return PropNegationFormula(self.visit(formula.body))

    @override
    def visit_connective(self, formula: PropConnectiveFormula) -> PropFormula:
        return PropConnectiveFormula(
            formula.conn,
            self.visit(formula.left),
            self.visit(formula.right)
        )
