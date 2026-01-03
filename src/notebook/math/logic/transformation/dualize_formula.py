from dataclasses import dataclass
from typing import override

from ..alphabet import BinaryConnective, get_dual_prop_constant, get_dual_quantifier
from ..formulas import (
    ConnectiveFormula,
    EqualityFormula,
    Formula,
    FormulaTransformationVisitor,
    NegationFormula,
    PredicateApplication,
    PropConstant,
    QuantifierFormula,
)
from ..propositional import PropFormula, convert_to_prop_formula
from .collapse_repeated_negation import collapse_repeated_negation


@dataclass(frozen=True)
class FormulaDualizationVisitor(FormulaTransformationVisitor):
    @override
    def visit_prop_constant(self, formula: PropConstant) -> PropConstant:
        return PropConstant(get_dual_prop_constant(formula.value))

    @override
    def visit_equality(self, formula: EqualityFormula) -> Formula:
        return NegationFormula(formula)

    @override
    def visit_predicate(self, formula: PredicateApplication) -> Formula:
        return NegationFormula(formula)

    @override
    def visit_negation(self, formula: NegationFormula) -> Formula:
        return collapse_repeated_negation(NegationFormula(self.visit(formula.body)))

    @override
    def visit_conjunction(self, formula: ConnectiveFormula) -> Formula:
        dual_left = self.visit(formula.left)
        dual_right = self.visit(formula.right)
        return ConnectiveFormula(BinaryConnective.DISJUNCTION, dual_left, dual_right)

    @override
    def visit_disjunction(self, formula: ConnectiveFormula) -> Formula:
        dual_left = self.visit(formula.left)
        dual_right = self.visit(formula.right)
        return ConnectiveFormula(BinaryConnective.CONJUNCTION, dual_left, dual_right)

    @override
    def visit_conditional(self, formula: ConnectiveFormula) -> Formula:
        return NegationFormula(collapse_repeated_negation(formula))

    @override
    def visit_biconditional(self, formula: ConnectiveFormula) -> Formula:
        return NegationFormula(collapse_repeated_negation(formula))

    @override
    def visit_quantifier(self, formula: QuantifierFormula) -> QuantifierFormula:
        dual_body = self.visit(formula.body)
        return QuantifierFormula(get_dual_quantifier(formula.quant), formula.var, dual_body)


def dualize_formula(formula: Formula) -> Formula:
    return FormulaDualizationVisitor().visit(formula)


# This is alg:propositional_formula_dualization in the monograph
def dualize_formula_prop(formula: PropFormula) -> PropFormula:
    return convert_to_prop_formula(dualize_formula(formula))
