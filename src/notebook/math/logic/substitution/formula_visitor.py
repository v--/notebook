from collections.abc import Mapping
from dataclasses import dataclass
from typing import override

from ..formulas import (
    EqualityFormula,
    Formula,
    FormulaTransformationVisitor,
    FormulaWithSubstitution,
    PredicateFormula,
    QuantifierFormula,
)
from ..terms import Term, Variable
from .substitution import LogicSubstitution, infer_substitution
from .term_visitor import TermSubstitutionVisitor


@dataclass(frozen=True)
class FormulaSubstitutionVisitor(FormulaTransformationVisitor):
    substitution: LogicSubstitution

    @override
    def visit_equality(self, formula: EqualityFormula) -> EqualityFormula:
        term_visitor = TermSubstitutionVisitor(self.substitution)
        return EqualityFormula(term_visitor.visit(formula.left), term_visitor.visit(formula.right))

    @override
    def visit_predicate(self, formula: PredicateFormula) -> PredicateFormula:
        term_visitor = TermSubstitutionVisitor(self.substitution)
        return PredicateFormula(formula.name, [term_visitor.visit(arg) for arg in formula.arguments])

    def visit_quantifier(self, formula: QuantifierFormula) -> QuantifierFormula:
        new_var = self.substitution.get_modified_quantifier_variable(formula)
        new_subst = self.substitution.modify_at(formula.var, new_var)
        new_subformula = apply_formula_substitution(formula.body, new_subst)
        return QuantifierFormula(formula.quantifier, new_var, new_subformula)


def apply_formula_substitution(formula: Formula, substitution: LogicSubstitution) -> Formula:
    return FormulaSubstitutionVisitor(substitution).visit(formula)


def substitute_in_formula(formula: Formula, variable_mapping: Mapping[Variable, Term]) -> Formula:
    return apply_formula_substitution(formula, LogicSubstitution(variable_mapping=variable_mapping))


def evaluate_substitution_spec(spec: FormulaWithSubstitution) -> Formula:
    if spec.sub is None:
        return spec.formula

    return apply_formula_substitution(spec.formula, infer_substitution(spec))


def unwrap_substitution_spec(spec: FormulaWithSubstitution) -> Formula:
    if spec.sub is None:
        return spec.formula

    return spec.formula
