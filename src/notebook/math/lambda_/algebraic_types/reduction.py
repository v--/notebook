from dataclasses import dataclass
from typing import override

from ..arrow_types import ARROW_ONLY_TYPE_SYSTEM
from ..assertions import VariableTypeAssertion
from ..terms import (
    TypedAbstraction,
    TypedApplication,
    TypedTerm,
)
from ..type_derivation import (
    AssumptionTree,
    RuleApplicationTree,
    TypeDerivationError,
    TypeDerivationTree,
    apply,
    assume,
    premise_config,
)
from ..variables import get_free_variables
from .alpha import alpha_convert_derivation
from .substitution import substitute_in_tree
from .visitor import SimpleAlgebraicDerivationTreeVisitor


class NotReducible(BaseException):
    pass


@dataclass
class ReductionVisitor(SimpleAlgebraicDerivationTreeVisitor[TypeDerivationTree]):
    reduct: TypedTerm

    @override
    def visit_assumption(self, tree: AssumptionTree) -> TypeDerivationTree:
        raise NotReducible

    @override
    def visit_arrow_intro(
        self,
        tree: RuleApplicationTree,
        subtree: TypeDerivationTree,
        subtree_discharge: VariableTypeAssertion,
    ) -> TypeDerivationTree:
        body = subtree.conclusion.term
        var = subtree_discharge.term
        var_type = subtree_discharge.type

        # η-reduction
        if isinstance(body, TypedApplication) and body.right == var and var not in get_free_variables(body.left):
            if not isinstance(subtree, RuleApplicationTree) or subtree.rule != ARROW_ONLY_TYPE_SYSTEM['→₋']:
                raise TypeDerivationError(f'Expected the tree deriving {subtree.conclusion} to be an application tree of →₋')

            try:
                return alpha_convert_derivation(subtree.premises[0].tree, self.reduct)
            except TypeDerivationError:
                pass

        # Recursion
        if isinstance(self.reduct, TypedAbstraction) and var_type == self.reduct.var_type:
            assertion = VariableTypeAssertion(self.reduct.var, self.reduct.var_type)

            if var == self.reduct.var:
                adjusted_subtree = subtree
            else:
                if self.reduct.var in get_free_variables(body):
                    raise NotReducible

                adjusted_subtree = substitute_in_tree(
                    subtree,
                    {var: assume(assertion)}
                )

            return apply(
                ARROW_ONLY_TYPE_SYSTEM['→₊'],
                premise_config(
                    attachments=[assertion],
                    tree=reduce_derivation_unsafe(adjusted_subtree, self.reduct.body)
                )
            )

        raise NotReducible

    @override
    def visit_arrow_elim(
        self,
        tree: RuleApplicationTree,
        subtree_left: TypeDerivationTree,
        subtree_right: TypeDerivationTree,
    ) -> TypeDerivationTree:
        left_term = subtree_left.conclusion.term

        # β-reduction
        if isinstance(left_term, TypedAbstraction):
            if not isinstance(subtree_left, RuleApplicationTree) or subtree_left.rule != ARROW_ONLY_TYPE_SYSTEM['→₊']:
                raise TypeDerivationError(f'Expected the tree deriving {subtree_left.conclusion} to be an application tree of →₊')

            assert subtree_left.premises[0].attachments[0]
            subtree_left_body = subtree_left.premises[0].tree
            subtree_left_var = subtree_left.premises[0].attachments[0].term
            reduct_tree = substitute_in_tree(subtree_left_body, {subtree_left_var: subtree_right})

            try:
                return alpha_convert_derivation(reduct_tree, self.reduct)
            except TypeDerivationError:
                pass

        # Recursion
        if isinstance(self.reduct, TypedApplication):
            try:
                result_subtree_left = alpha_convert_derivation(subtree_left, self.reduct.left)
            except TypeDerivationError:
                pass
            else:
                return apply(
                    ARROW_ONLY_TYPE_SYSTEM['→₋'],
                    result_subtree_left,
                    reduce_derivation_unsafe(subtree_right, self.reduct.right)
                )

            try:
                result_subtree_right = alpha_convert_derivation(subtree_right, self.reduct.right)
            except TypeDerivationError:
                pass
            else:
                return apply(
                    ARROW_ONLY_TYPE_SYSTEM['→₋'],
                    reduce_derivation_unsafe(subtree_left, self.reduct.left),
                    result_subtree_right,
                )

        raise NotReducible

    @override
    def visit_rule_application(self, tree: RuleApplicationTree) -> TypeDerivationTree:
        raise TypeDerivationError('Only arrow types are supported for typed βη-reduction')


def reduce_derivation_unsafe(tree: TypeDerivationTree, reduct: TypedTerm) -> TypeDerivationTree:
    return ReductionVisitor(reduct).visit(tree)


# This is alg:simply_typed_reduction in the monograph
def reduce_derivation(tree: TypeDerivationTree, reduct: TypedTerm) -> TypeDerivationTree:
    try:
        return reduce_derivation_unsafe(tree, reduct)
    except NotReducible:
        raise TypeDerivationError(f'The term {tree.conclusion.term} is not βη-reducible to {reduct} in one step') from None
