from typing import TYPE_CHECKING, override

from notebook.math.lambda_.terms import TypedAbstraction, TypedTerm, Variable
from notebook.math.lambda_.type_derivation.tree import TypeDerivationTree
from notebook.math.lambda_.variables import get_free_variables, new_variable
from notebook.support.substitution import AbstractAtomicSubstitution, UnspecifiedReplacementError


if TYPE_CHECKING:
    from collections.abc import Collection, Iterable, Mapping


class AtomicTypeDerivationSubstitution(AbstractAtomicSubstitution[Variable, TypeDerivationTree]):
    variable_mapping: Mapping[Variable, TypeDerivationTree]

    def __init__(self, *, variable_mapping: Mapping[Variable, TypeDerivationTree] | None = None) -> None:
        self.variable_mapping = variable_mapping or {}

    @override
    def generate_fresh_variable(self, blacklist: Collection[Variable]) -> Variable:
        return new_variable(blacklist)

    @override
    def substitute_variable(self, var: Variable) -> TypeDerivationTree:
        try:
            return self.variable_mapping[var]
        except KeyError:
            raise UnspecifiedReplacementError(f'No substitution nor type given for variable {var.identifier}') from None

    def iter_free_in_substituted_for_term(self, term: TypedTerm) -> Iterable[Variable]:
        for var in get_free_variables(term):
            try:
                replacement = self.variable_mapping[var]
            except KeyError:
                yield var
            else:
                yield from get_free_variables(replacement.conclusion.term)

    def iter_free_in_substituted(self, tree: TypeDerivationTree) -> Iterable[Variable]:
        return self.iter_free_in_substituted_for_term(tree.conclusion.term)

    def get_modified_abstractor_variable(self, term: TypedAbstraction) -> Variable:
        blacklist = set(self.iter_free_in_substituted_for_term(term))

        if term.var in blacklist:
            return self.generate_fresh_variable(blacklist)

        return term.var

    @override
    def modify_at(self, var: Variable, replacement: TypeDerivationTree) -> AtomicTypeDerivationSubstitution:
        return AtomicTypeDerivationSubstitution(variable_mapping={**self.variable_mapping, var: replacement})

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AtomicTypeDerivationSubstitution):
            return NotImplemented

        return self.variable_mapping == other.variable_mapping

    def __hash__(self) -> int:
        return hash(self.variable_mapping)

    def __str__(self) -> str:
        return '[' + ', '.join(f'{key} ↦ {value}' for key, value in self.variable_mapping.items()) + ']'

    def __repr__(self) -> str:
        return str(self)
