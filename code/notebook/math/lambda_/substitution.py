from collections.abc import Collection, Iterable, Mapping
from dataclasses import dataclass
from typing import Protocol, override

from ...support.iteration import iter_accumulator
from .exceptions import LambdaCalculusError
from .terms import Constant, UntypedAbstraction, UntypedApplication, UntypedTerm, UntypedTermVisitor, Variable
from .variables import get_free_variables, new_variable


class SubstitutionError(LambdaCalculusError):
    pass


class AbstractTermSubstitution(Protocol):
    def get_non_fixed(self) -> Collection[Variable]:
        ...

    def generate_new_variable(self, context: Collection[Variable]) -> Variable:
        ...


class TermSubstitution(AbstractTermSubstitution):
    variable_mapping: Mapping[Variable, UntypedTerm]

    def __init__(self, *, variable_mapping: Mapping[Variable, UntypedTerm] | None = None) -> None:
        self.variable_mapping = variable_mapping or {}

    @override
    def get_non_fixed(self) -> Collection[Variable]:
        return {var for var, term in self.variable_mapping.items() if var != term}

    @override
    def generate_new_variable(self, context: Collection[Variable]) -> Variable:
        return new_variable(context)

    def substitute_variable(self, var: Variable) -> UntypedTerm:
        return self.variable_mapping.get(var, var)

    @iter_accumulator(frozenset)
    def get_free_in_substituted(self, term: UntypedTerm) -> Iterable[Variable]:
        for var in get_free_variables(term):
            yield from get_free_variables(self.substitute_variable(var))

    def modify_at(self, var: Variable, replacement: UntypedTerm) -> 'TermSubstitution':
        return TermSubstitution(variable_mapping={**self.variable_mapping, var: replacement})


EMPTY_SUBSTITUTION = TermSubstitution()


@dataclass(frozen=True)
class TermSubstitutionApplicationVisitor(UntypedTermVisitor[UntypedTerm]):
    substitution: TermSubstitution

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
        if term.var in self.substitution.get_free_in_substituted(term):
            context = {
                *get_free_variables(term.sub),
                *self.substitution.get_free_in_substituted(term.sub),
                *self.substitution.get_non_fixed()
            }

            new_var = self.substitution.generate_new_variable(context)
        else:
            new_var = term.var

        new_sub = self.substitution.modify_at(term.var, new_var)

        return UntypedAbstraction(
            new_var,
            TermSubstitutionApplicationVisitor(new_sub).visit(term.sub),
        )


def apply_term_substitution(term: UntypedTerm, substitution: TermSubstitution) -> UntypedTerm:
    return TermSubstitutionApplicationVisitor(substitution).visit(term)
