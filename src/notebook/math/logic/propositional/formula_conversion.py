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
from .exceptions import NonPropositionalFormulaError
from .formulas import PropConnectiveFormula, PropFormula, PropNegationFormula, PropVariable
from .symbols import PropVariableSymbol


class PropFormulaConversionVisitor(FormulaVisitor[PropFormula]):
    @override
    def visit_prop_constant(self, formula: PropConstant) -> PropConstant:
        return formula

    @override
    def visit_equality(self, formula: EqualityFormula) -> PropFormula:
        raise NonPropositionalFormulaError(f'Unexpected equality {formula} in propositional formula')

    @override
    def visit_predicate(self, formula: PredicateApplication) -> PropVariable:
        if not isinstance(formula.symbol, PropVariableSymbol):
            raise NonPropositionalFormulaError(f'Unexpected predicate application {formula} in propositional formula')

        return PropVariable(formula.symbol)

    @override
    def visit_negation(self, formula: NegationFormula) -> PropNegationFormula:
        return PropNegationFormula(self.visit(formula.body))

    @override
    def visit_connective(self, formula: ConnectiveFormula) -> PropConnectiveFormula:
        return PropConnectiveFormula(
            formula.conn,
            self.visit(formula.left),
            self.visit(formula.right)
        )

    @override
    def visit_quantifier(self, formula: QuantifierFormula) -> PropFormula:
        raise NonPropositionalFormulaError(f'Unexpected quantifier {formula.quant} in propositional formula')


def convert_to_prop_formula(formula: Formula) -> PropFormula:
    return PropFormulaConversionVisitor().visit(formula)
