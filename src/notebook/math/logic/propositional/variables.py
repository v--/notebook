from collections.abc import Collection
from typing import override

from ..formulas import ConnectiveFormula, ConstantFormula, Formula, NegationFormula
from .formula_visitor import PropositionalFormulaVisitor
from .formulas import PropositionalVariable, PropositionalVariableFormula, extract_variable


class VariableVisitor(PropositionalFormulaVisitor[Collection[PropositionalVariable]]):
    @override
    def visit_logical_constant(self, formula: ConstantFormula) -> Collection[PropositionalVariable]:
        return set()

    @override
    def visit_propositional_variable(self, formula: PropositionalVariableFormula) -> Collection[PropositionalVariable]:
        return {extract_variable(formula)}

    @override
    def visit_negation(self, formula: NegationFormula) -> Collection[PropositionalVariable]:
        return self.visit(formula.body)

    @override
    def visit_connective(self, formula: ConnectiveFormula) -> Collection[PropositionalVariable]:
        return {*self.visit(formula.left), *self.visit(formula.right)}


def get_propositional_variables(formula: Formula) -> Collection[PropositionalVariable]:
    return VariableVisitor().visit(formula)
