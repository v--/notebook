from collections.abc import Mapping
from dataclasses import dataclass
from typing import override

from ..terms import FunctionApplication, Term, TermTransformationVisitor, Variable
from .substitution import AtomicLogicSubstitution


@dataclass(frozen=True)
class TermSubstitutionVisitor(TermTransformationVisitor):
    substitution: AtomicLogicSubstitution

    @override
    def visit_variable(self, term: Variable) -> Term:
        return self.substitution.substitute_variable(term)

    @override
    def visit_function(self, term: FunctionApplication) -> Term:
        return FunctionApplication(term.symbol, [self.visit(arg) for arg in term.arguments])


# This is alg:fol_substitution/terms in the monograph
def apply_substitution_to_term(term: Term, substitution: AtomicLogicSubstitution) -> Term:
    return TermSubstitutionVisitor(substitution).visit(term)


def substitute_in_term(term: Term, variable_mapping: Mapping[Variable, Term]) -> Term:
    return apply_substitution_to_term(term, AtomicLogicSubstitution(variable_mapping=variable_mapping))
