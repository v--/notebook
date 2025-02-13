from collections.abc import Collection, Iterable, Mapping
from typing import override

from ....support.substitution import AbstractSubstitution, UnspecifiedReplacementError
from ..assertions import VariableTypeAssertion
from ..terms import (
    TypedAbstraction,
    Variable,
)
from ..type_systems import ARROW_ELIM_RULE_EXPLICIT, ARROW_INTRO_RULE_EXPLICIT
from ..variables import get_free_variables, new_variable
from .exceptions import TypeDerivationError, UnknownDerivationRuleError
from .tree import AssumptionTree, RuleApplicationTree, TypeDerivationTree, apply, assume, premise


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


# This is def:lambda_substitution in the monograph
def apply_tree_substitution(tree: TypeDerivationTree, substitution: TypeDerivationSubstitution) -> TypeDerivationTree:
    if isinstance(tree, AssumptionTree):
        try:
            dest = substitution.substitute_variable(tree.conclusion.term)
        except UnspecifiedReplacementError:
            return tree

        if dest.conclusion.type != tree.conclusion.type:
            raise TypeDerivationError(f'Cannot substitute {tree.conclusion} for {dest.conclusion} in {tree.conclusion} due to incompatible types')

        return dest

    if isinstance(tree, RuleApplicationTree):
        if tree.rule == ARROW_ELIM_RULE_EXPLICIT:
            return apply(
                ARROW_ELIM_RULE_EXPLICIT,
                apply_tree_substitution(tree.premises[0].tree, substitution),
                apply_tree_substitution(tree.premises[1].tree, substitution)
            )

        if tree.rule == ARROW_INTRO_RULE_EXPLICIT:
            term = tree.conclusion.term
            assert isinstance(term, TypedAbstraction)

            application_premise = tree.premises[0]

            if term.var in substitution.iter_free_in_substituted(tree):
                new_var = substitution.generate_fresh_variable(
                    set(substitution.iter_free_in_substituted(application_premise.tree))
                )
            else:
                new_var = term.var

            new_var_tree = assume(VariableTypeAssertion(new_var, term.var_type))

            return apply(
                ARROW_INTRO_RULE_EXPLICIT,
                premise(
                    tree=apply_tree_substitution(application_premise.tree, substitution.modify_at(term.var, new_var_tree)),
                    discharge=new_var_tree.conclusion
                )
            )

        raise UnknownDerivationRuleError(f'Unknown rule {tree.rule.name}')

    return tree


def substitute(tree: TypeDerivationTree, variable_mapping: Mapping[Variable, TypeDerivationTree]) -> TypeDerivationTree:
    return apply_tree_substitution(tree, TypeDerivationSubstitution(variable_mapping=variable_mapping))
