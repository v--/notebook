from dataclasses import dataclass
from typing import TYPE_CHECKING, override

from notebook.math.lambda_.terms import (
    Constant,
    UntypedAbstraction,
    UntypedApplication,
    UntypedTerm,
    UntypedTermVisitor,
    Variable,
)
from notebook.support.coderefs import collector

from .substitution import UntypedTermSubstitution


if TYPE_CHECKING:
    from collections.abc import Mapping


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


@collector.ref('alg:lambda_term_substitution')
def apply_substitution_to_term(term: UntypedTerm, substitution: UntypedTermSubstitution) -> UntypedTerm:
    return UntypedSubstitutionApplicationVisitor(substitution).visit(term)


def substitute(term: UntypedTerm, variable_mapping: Mapping[Variable, UntypedTerm]) -> UntypedTerm:
    return apply_substitution_to_term(term, UntypedTermSubstitution(variable_mapping=variable_mapping))
