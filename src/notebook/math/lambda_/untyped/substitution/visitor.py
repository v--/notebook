from collections.abc import Mapping
from dataclasses import dataclass
from typing import override

from ...terms import (
    Constant,
    UntypedAbstraction,
    UntypedApplication,
    UntypedTerm,
    UntypedTermVisitor,
    Variable,
)
from .substitution import UntypedTermSubstitution


@dataclass(frozen=True)
class UntypedSubstitutionApplicationVisitor(UntypedTermVisitor[UntypedTerm]):
    substitution: UntypedTermSubstitution

    @override
    def visit_constant(self, term: Constant) -> Constant:
        return term

    @override
    def visit_variable(self, term: Variable) -> UntypedTerm:
        return self.substitution.substitute_variable(term)

    @override
    def visit_application(self, term: UntypedApplication) -> UntypedApplication:
        return UntypedApplication(self.visit(term.left), self.visit(term.right))

    @override
    def visit_abstraction(self, term: UntypedAbstraction) -> UntypedAbstraction:
        new_var = self.substitution.get_modified_abstractor_variable(term)
        new_subst = self.substitution.modify_at(term.var, new_var)
        new_subterm = apply_substitution_to_term(term.body, new_subst)
        return UntypedAbstraction(new_var, new_subterm)


# This is alg:lambda_term_substitution in the monograph
def apply_substitution_to_term(term: UntypedTerm, substitution: UntypedTermSubstitution) -> UntypedTerm:
    return UntypedSubstitutionApplicationVisitor(substitution).visit(term)


def substitute(term: UntypedTerm, variable_mapping: Mapping[Variable, UntypedTerm]) -> UntypedTerm:
    return apply_substitution_to_term(term, UntypedTermSubstitution(variable_mapping=variable_mapping))
