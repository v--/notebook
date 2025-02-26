from collections.abc import Collection, Iterable, Mapping  # noqa: I001
from dataclasses import dataclass
from typing import override

from ....support.substitution import AbstractSubstitution, UnspecifiedReplacementError
from ..assertions import VariableTypeAssertion
from ..terms import (
    TypedApplication,
    TypedAbstraction,
    Variable,
)
from ..type_systems import ARROW_ELIM_RULE_EXPLICIT, ARROW_INTRO_RULE_EXPLICIT
from ..variables import get_free_variables, new_variable
from .exceptions import TypeDerivationError
from .tree import AssumptionTree, RuleApplicationTree, TypeDerivationTree, apply, assume, premise
from .visitors import BasicDerivationTreeVisitor


class TypeDerivationSubstitution(AbstractSubstitution[Variable, TypeDerivationTree]):
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
            raise UnspecifiedReplacementError(f'No substitution nor type given for variable {var}') from None

    def iter_free_in_substituted(self, tree: TypeDerivationTree) -> Iterable[Variable]:
        for var in get_free_variables(tree.conclusion.term):
            try:
                replacement = self.variable_mapping[var]
            except KeyError:
                yield var
            else:
                yield from get_free_variables(replacement.conclusion.term)

    @override
    def modify_at(self, var: Variable, replacement: TypeDerivationTree) -> 'TypeDerivationSubstitution':
        return TypeDerivationSubstitution(variable_mapping={**self.variable_mapping, var: replacement})


@dataclass
class TreeSubstitutionVisitor(BasicDerivationTreeVisitor[TypeDerivationTree]):
    substitution: TypeDerivationSubstitution

    @override
    def visit_assumption(self, tree: AssumptionTree) -> TypeDerivationTree:
        try:
            dest = self.substitution.substitute_variable(tree.conclusion.term)
        except UnspecifiedReplacementError:
            return tree

        if dest.conclusion.type != tree.conclusion.type:
            raise TypeDerivationError(f'Cannot substitute {tree.conclusion} for {dest.conclusion} in {tree.conclusion} due to incompatible types')

        return dest

    @override
    def visit_arrow_elim(
        self,
        tree: RuleApplicationTree,
        subtree_left: TypeDerivationTree,
        subtree_right: TypeDerivationTree,
        term: TypedApplication
    ) -> RuleApplicationTree:
        return apply(
            ARROW_ELIM_RULE_EXPLICIT,
            self.visit(subtree_left),
            self.visit(subtree_right)
        )

    @override
    def visit_arrow_intro(
        self,
        tree: RuleApplicationTree,
        subtree: TypeDerivationTree,
        discharge: VariableTypeAssertion,
        term: TypedAbstraction
    ) -> RuleApplicationTree:
        if term.var in self.substitution.iter_free_in_substituted(tree):
            new_var = self.substitution.generate_fresh_variable(
                set(self.substitution.iter_free_in_substituted(subtree))
            )
        else:
            new_var = term.var

        new_var_tree = assume(VariableTypeAssertion(new_var, term.var_type))

        return apply(
            ARROW_INTRO_RULE_EXPLICIT,
            premise(
                tree=apply_tree_substitution(subtree, self.substitution.modify_at(term.var, new_var_tree)),
                discharge=new_var_tree.conclusion
            )
        )


# This is def:lambda_term_substitution in the monograph
def apply_tree_substitution(tree: TypeDerivationTree, substitution: TypeDerivationSubstitution) -> TypeDerivationTree:
    return TreeSubstitutionVisitor(substitution).visit(tree)


def substitute(tree: TypeDerivationTree, variable_mapping: Mapping[Variable, TypeDerivationTree]) -> TypeDerivationTree:
    return apply_tree_substitution(tree, TypeDerivationSubstitution(variable_mapping=variable_mapping))
