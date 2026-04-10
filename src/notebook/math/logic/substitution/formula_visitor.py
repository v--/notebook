from dataclasses import dataclass
from typing import TYPE_CHECKING, override

from ....support.coderefs import collector
from ..formulas import (
    EqualityFormula,
    Formula,
    FormulaTransformationVisitor,
    FormulaWithSubstitution,
    PredicateApplication,
    QuantifierFormula,
)
from .substitution import AtomicLogicSubstitution, infer_substitution
from .term_visitor import TermSubstitutionVisitor


if TYPE_CHECKING:
    from collections.abc import Mapping

    from ..terms import Term, Variable


@dataclass(frozen=True)
class FormulaSubstitutionVisitor(FormulaTransformationVisitor):
    substitution: AtomicLogicSubstitution

    @override
    def visit_equality(self, formula: EqualityFormula) -> EqualityFormula:
        term_visitor = TermSubstitutionVisitor(self.substitution)
        return EqualityFormula(term_visitor.visit(formula.left), term_visitor.visit(formula.right))

    @override
    def visit_predicate(self, formula: PredicateApplication) -> PredicateApplication:
        term_visitor = TermSubstitutionVisitor(self.substitution)
        return PredicateApplication(formula.symbol, [term_visitor.visit(arg) for arg in formula.arguments])

    def visit_quantifier(self, formula: QuantifierFormula) -> QuantifierFormula:
        new_var = self.substitution.get_modified_quantifier_variable(formula)
        new_subst = self.substitution.modify_at(formula.var, new_var)
        new_subformula = apply_substitution_to_formula(formula.body, new_subst)
        return QuantifierFormula(formula.quant, new_var, new_subformula)


@collector.ref('alg:fol_formula_substitution')
def apply_substitution_to_formula(formula: Formula, substitution: AtomicLogicSubstitution) -> Formula:
    return FormulaSubstitutionVisitor(substitution).visit(formula)


def substitute_in_formula(formula: Formula, variable_mapping: Mapping[Variable, Term]) -> Formula:
    return apply_substitution_to_formula(formula, AtomicLogicSubstitution(variable_mapping=variable_mapping))


def evaluate_substitution(spec: Formula | FormulaWithSubstitution) -> Formula:
    if isinstance(spec, FormulaWithSubstitution):
        return apply_substitution_to_formula(spec.formula, infer_substitution(spec))

    return spec
