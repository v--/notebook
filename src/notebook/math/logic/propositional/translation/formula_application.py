from dataclasses import dataclass
from typing import TYPE_CHECKING, override

from .....support.coderefs import collector
from ...formulas import ConnectiveFormula, Formula, NegationFormula, PropConstant
from ..formula_visitor import PropFormulaVisitor
from .base import PropFormulaTranslation


if TYPE_CHECKING:
    from collections.abc import Mapping

    from ..formulas import PropConnectiveFormula, PropFormula, PropNegationFormula, PropVariable


@dataclass(frozen=True)
class FormulaSubstitutionVisitor(PropFormulaVisitor[Formula]):
    translation: PropFormulaTranslation

    @override
    def visit_prop_constant(self, formula: PropConstant) -> PropConstant:
        return formula

    @override
    def visit_variable(self, formula: PropVariable) -> Formula:
        return self.translation.translate_variable(formula)

    @override
    def visit_negation(self, formula: PropNegationFormula) -> NegationFormula:
        return NegationFormula(self.visit(formula.body))

    @override
    def visit_connective(self, formula: PropConnectiveFormula) -> ConnectiveFormula:
        return ConnectiveFormula(
            formula.conn,
            self.visit(formula.left),
            self.visit(formula.right),
        )


@collector.ref('alg:fol_propositional_formula_translation')
def apply_prop_formula_translation(formula: PropFormula, translation: PropFormulaTranslation) -> Formula:
    return FormulaSubstitutionVisitor(translation).visit(formula)


def translate_prop_formula(formula: PropFormula, mapping: Mapping[PropVariable, Formula]) -> Formula:
    return apply_prop_formula_translation(formula, PropFormulaTranslation(mapping))
