from collections.abc import Collection, Iterable, Mapping
from dataclasses import dataclass
from typing import override

from ....support.substitution import AbstractSubstitution
from ..terms import (
    Constant,
    UntypedAbstraction,
    UntypedApplication,
    UntypedTerm,
    UntypedTermVisitor,
    Variable,
)
from ..variables import get_free_variables, new_variable


class UntypedTermSubstitution(AbstractSubstitution[Variable, UntypedTerm]):
    variable_mapping: Mapping[Variable, UntypedTerm]

    def __init__(self, *, variable_mapping: Mapping[Variable, UntypedTerm] | None = None) -> None:
        self.variable_mapping = variable_mapping or {}

    @override
    def generate_fresh_variable(self, blacklist: Collection[Variable]) -> Variable:
        return new_variable(blacklist)

    @override
    def substitute_variable(self, var: Variable) -> UntypedTerm:
        return self.variable_mapping.get(var, var)

    def iter_free_in_substituted(self, term: UntypedTerm) -> Iterable[Variable]:
        for var in get_free_variables(term):
            yield from get_free_variables(self.substitute_variable(var))

    @override
    def modify_at(self, var: Variable, replacement: UntypedTerm) -> 'UntypedTermSubstitution':
        return UntypedTermSubstitution(variable_mapping={**self.variable_mapping, var: replacement})


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
        return UntypedApplication(self.visit(term.a), self.visit(term.b))

    @override
    def visit_abstraction(self, term: UntypedAbstraction) -> UntypedAbstraction:
        if term.var in self.substitution.iter_free_in_substituted(term):
            new_var = self.substitution.generate_fresh_variable(
                set(self.substitution.iter_free_in_substituted(term.sub))
            )
        else:
            new_var = term.var

        new_sub = self.substitution.modify_at(term.var, new_var)

        return UntypedAbstraction(
            new_var,
            apply_term_substitution(term.sub, new_sub)
        )


# This is alg:simply_typed_substitution in the monograph
def apply_term_substitution(term: UntypedTerm, substitution: UntypedTermSubstitution) -> UntypedTerm:
    return UntypedSubstitutionApplicationVisitor(substitution).visit(term)


def substitute(term: UntypedTerm, variable_mapping: Mapping[Variable, UntypedTerm]) -> UntypedTerm:
    return apply_term_substitution(term, UntypedTermSubstitution(variable_mapping=variable_mapping))
