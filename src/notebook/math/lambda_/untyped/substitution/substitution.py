from collections.abc import Collection, Iterable, Mapping
from typing import override

from .....support.substitution import AbstractSubstitution
from ...terms import UntypedAbstraction, UntypedTerm, Variable
from ...variables import get_free_variables, new_variable


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

    def get_modified_abstractor_variable(self, term: UntypedAbstraction) -> Variable:
        blacklist = set(self.iter_free_in_substituted(term))

        if term.var in blacklist:
            return self.generate_fresh_variable(blacklist)

        return term.var

    @override
    def modify_at(self, var: Variable, replacement: UntypedTerm) -> UntypedTermSubstitution:
        return UntypedTermSubstitution(variable_mapping={**self.variable_mapping, var: replacement})
