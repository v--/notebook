from typing import override

from ..formulas import (
    ConnectiveFormula,
    ConstantFormula,
    EqualityFormula,
    Formula,
    FormulaVisitor,
    NegationFormula,
    PredicateApplication,
    QuantifierFormula,
)
from .exceptions import NonPropositionalFormulaError
from .formulas import PropositionalVariable, PropositionalVariableFormula


class PropositionalFormulaVisitor[T](FormulaVisitor[T]):
    @override
    def visit_equality(self, formula: EqualityFormula) -> T:
        raise NonPropositionalFormulaError(f'Unexpected equality {formula} in propositional formula')

    @override
    def visit_predicate(self, formula: PredicateApplication) -> T:
        if not isinstance(formula.symbol, PropositionalVariable):
            raise NonPropositionalFormulaError(f'Unexpected predicate application {formula} in propositional formula')

        return self.visit_propositional_variable(formula)

    def visit_propositional_variable(self, formula: PropositionalVariableFormula) -> T:
        return self.generic_visit(formula)

    @override
    def visit_quantifier(self, formula: QuantifierFormula) -> T:
        raise NonPropositionalFormulaError(f'Unexpected quantifier {formula.quantifier} in propositional formula')


class PropositionalFormulaTransformationVisitor(PropositionalFormulaVisitor[Formula]):
    @override
    def visit_logical_constant(self, formula: ConstantFormula) -> Formula:
        return formula

    @override
    def visit_propositional_variable(self, formula: PropositionalVariableFormula) -> Formula:
        return formula

    @override
    def visit_negation(self, formula: NegationFormula) -> Formula:
        return NegationFormula(self.visit(formula.body))

    @override
    def visit_connective(self, formula: ConnectiveFormula) -> Formula:
        return ConnectiveFormula(
            formula.conn,
            self.visit(formula.left),
            self.visit(formula.right)
        )
