from collections.abc import Mapping
from dataclasses import dataclass
from typing import override

from ....support.substitution import UnspecifiedReplacementError
from ..assertions import VariableTypeAssertion
from ..instantiation import AtomicLambdaSchemaInstantiation
from ..terms import TypedAbstraction, Variable
from ..type_derivation import (
    AssumptionTree,
    AtomicTypeDerivationSubstitution,
    RuleApplicationPremise,
    RuleApplicationTree,
    TypeDerivationError,
    TypeDerivationTree,
    apply,
    apply_tree_substitution_to_term,
    assume,
    premise,
)
from .visitor import SimpleAlgebraicDerivationTreeVisitor


@dataclass
class TreeSubstitutionVisitor(SimpleAlgebraicDerivationTreeVisitor[TypeDerivationTree]):
    substitution: AtomicTypeDerivationSubstitution

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
    def visit_rule_application(self, tree: RuleApplicationTree) -> RuleApplicationTree:
        term_mapping = {
            placeholder: apply_tree_substitution_to_term(term, self.substitution)
            for placeholder, term in tree.instantiation.term_mapping.items()
        }

        instantiation = AtomicLambdaSchemaInstantiation(
            term_mapping=term_mapping,
            type_mapping=tree.instantiation.type_mapping,
        )

        return apply(
            tree.rule,
            *(premise(tree=apply_substitution_to_tree(p.tree, self.substitution)) for p in tree.premises),
            instantiation=instantiation
        )

    def _visit_abstractor_premise(self, body_tree: TypeDerivationTree, assertion: VariableTypeAssertion) -> RuleApplicationPremise:
        abstraction = TypedAbstraction(assertion.term, assertion.type, body_tree.conclusion.term)
        new_var = self.substitution.get_modified_abstractor_variable(abstraction)
        new_assertion = VariableTypeAssertion(new_var, assertion.type)
        new_subst = self.substitution.modify_at(assertion.term, assume(new_assertion))
        return premise(
            tree=apply_substitution_to_tree(body_tree, new_subst),
            discharge=new_assertion
        )

    @override
    def visit_arrow_intro(
        self,
        tree: RuleApplicationTree,
        subtree: TypeDerivationTree,
        subtree_discharge: VariableTypeAssertion,
    ) -> RuleApplicationTree:
        new_premise = self._visit_abstractor_premise(subtree, subtree_discharge)

        # Unlike in the monograph, here we infer the instantiation needed to apply the rule
        return apply(
            tree.rule,
            new_premise,
        )

    @override
    def visit_sum_elim(
        self,
        tree: RuleApplicationTree,
        sum_subtree: TypeDerivationTree,
        left_subtree: TypeDerivationTree,
        left_subtree_discharge: VariableTypeAssertion,
        right_subtree: TypeDerivationTree,
        right_subtree_discharge: VariableTypeAssertion,
    ) -> RuleApplicationTree:
        new_sum_premise = premise(tree=apply_substitution_to_tree(sum_subtree, self.substitution))
        new_left_premise = self._visit_abstractor_premise(left_subtree, left_subtree_discharge)
        new_right_premise = self._visit_abstractor_premise(right_subtree, right_subtree_discharge)

        # Unlike in the monograph, here we infer the instantiation needed to apply the rule
        return apply(
            tree.rule,
            new_sum_premise, new_left_premise, new_right_premise,
        )


# This is def:atomic_lambda_term_substitution in the monograph
def apply_substitution_to_tree(tree: TypeDerivationTree, substitution: AtomicTypeDerivationSubstitution) -> TypeDerivationTree:
    return TreeSubstitutionVisitor(substitution).visit(tree)


def substitute_in_tree(tree: TypeDerivationTree, variable_mapping: Mapping[Variable, TypeDerivationTree]) -> TypeDerivationTree:
    return apply_substitution_to_tree(
        tree,
        AtomicTypeDerivationSubstitution(variable_mapping=variable_mapping)
    )
