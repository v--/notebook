from collections.abc import Iterable
from dataclasses import dataclass
from typing import Protocol, override

from ...support.iteration import frozen_set_accumulator
from .exceptions import LambdaError
from .terms import Abstraction, Application, LambdaTerm, Variable
from .variables import get_free_variables, new_variable
from .visitors import TermTransformationVisitor


class SubstitutionError(LambdaError):
    pass


class AbstractSubstitution(Protocol):
    def get_non_fixed(self) -> frozenset[Variable]:
        ...

    def generate_new_variable(self, context: frozenset[Variable]) -> Variable:
        ...


@dataclass
class Substitution(AbstractSubstitution):
    mapping: dict[Variable, LambdaTerm]

    @override
    def get_non_fixed(self) -> frozenset[Variable]:
        return frozenset(var for var, term in self.mapping.items() if var != term)

    @override
    def generate_new_variable(self, context: frozenset[Variable]) -> Variable:
        return new_variable(context)

    def substitute_variable(self, var: Variable) -> LambdaTerm:
        return self.mapping.get(var, var)

    @frozen_set_accumulator
    def get_free_in_substituted(self, term: LambdaTerm) -> Iterable[Variable]:
        for var in get_free_variables(term):
            yield from get_free_variables(self.substitute_variable(var))

    def modify_at(self, var: Variable, replacement: LambdaTerm) -> 'Substitution':
        return Substitution(self.mapping | { var: replacement })


EMPTY_SUBSTITUTION = Substitution({})


@dataclass
class SubstitutionApplicationVisitor(TermTransformationVisitor):
    substitution: Substitution

    @override
    def visit_variable(self, term: Variable) -> LambdaTerm:
        return self.substitution.substitute_variable(term)

    @override
    def visit_application(self, term: Application) -> Application:
        return Application(self.visit(term.a), self.visit(term.b))

    @override
    def visit_abstraction(self, term: Abstraction) -> Abstraction:
        if term.var in self.substitution.get_free_in_substituted(term):
            context = get_free_variables(term.sub) | self.substitution.get_free_in_substituted(term.sub) | self.substitution.get_non_fixed()
            new_var = self.substitution.generate_new_variable(context)
        else:
            new_var = term.var

        new_sub = self.substitution.modify_at(term.var, new_var)

        return Abstraction(
            new_var,
            SubstitutionApplicationVisitor(new_sub).visit(term.sub)
        )


def apply_substitution(term: LambdaTerm, substitution: Substitution) -> LambdaTerm:
    return SubstitutionApplicationVisitor(substitution).visit(term)
