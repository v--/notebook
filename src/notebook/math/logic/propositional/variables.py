from collections.abc import Collection
from typing import override

from ..formulas import PropConstant
from .formula_visitor import PropFormulaVisitor
from .formulas import (
    PropConnectiveFormula,
    PropFormula,
    PropNegationFormula,
    PropVariable,
)


class VariableVisitor(PropFormulaVisitor[Collection[PropVariable]]):
    @override
    def visit_prop_constant(self, formula: PropConstant) -> Collection[PropVariable]:
        return set()

    @override
    def visit_variable(self, formula: PropVariable) -> Collection[PropVariable]:
        return {formula}

    @override
    def visit_negation(self, formula: PropNegationFormula) -> Collection[PropVariable]:
        return self.visit(formula.body)

    @override
    def visit_connective(self, formula: PropConnectiveFormula) -> Collection[PropVariable]:
        return {*self.visit(formula.left), *self.visit(formula.right)}


def get_prop_variables(formula: PropFormula) -> Collection[PropVariable]:
    return VariableVisitor().visit(formula)
