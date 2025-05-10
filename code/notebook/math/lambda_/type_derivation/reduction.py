from dataclasses import dataclass
from typing import override

from ..assertions import VariableTypeAssertion
from ..terms import (
    TypedAbstraction,
    TypedApplication,
    TypedTerm,
)
from ..type_system import BASE_EXPLICIT_TYPE_SYSTEM
from ..variables import get_free_variables
from .alpha import alpha_convert_derivation
from .exceptions import TypeDerivationError
from .substitution import substitute
from .tree import AssumptionTree, RuleApplicationTree, TypeDerivationTree, apply, assume, premise
from .visitors import BasicDerivationTreeVisitor


class NotReducible(BaseException):
    pass


@dataclass
class ReductionVisitor(BasicDerivationTreeVisitor[TypeDerivationTree]):
    reduct: TypedTerm

    @override
    def visit_assumption(self, tree: AssumptionTree) -> TypeDerivationTree:
        raise NotReducible

    @override
    def visit_arrow_elim(
        self,
        tree: RuleApplicationTree,
        subtree_left: TypeDerivationTree,
        subtree_right: TypeDerivationTree,
        term: TypedApplication
    ) -> TypeDerivationTree:
        left_term = subtree_left.conclusion.term

        # β-reduction
        if isinstance(left_term, TypedAbstraction):
            assert isinstance(subtree_left, RuleApplicationTree)
            reduct_tree = substitute(subtree_left.premises[0].tree, {left_term.var: subtree_right})

            try:
                return alpha_convert_derivation(reduct_tree, self.reduct)
            except TypeDerivationError:
                pass

        # Recursion
        if isinstance(self.reduct, TypedApplication):
            try:
                result_subtree_left = alpha_convert_derivation(subtree_left, self.reduct.a)
            except TypeDerivationError:
                pass
            else:
                return apply(
                    BASE_EXPLICIT_TYPE_SYSTEM, '→₋',
                    result_subtree_left,
                    ReductionVisitor(self.reduct.b).visit(subtree_right)
                )

            try:
                result_subtree_right = alpha_convert_derivation(subtree_right, self.reduct.b)
            except TypeDerivationError:
                pass
            else:
                return apply(
                    BASE_EXPLICIT_TYPE_SYSTEM, '→₋',
                    ReductionVisitor(self.reduct.a).visit(subtree_left),
                    result_subtree_right,
                )

        raise NotReducible

    @override
    def visit_arrow_intro(
        self,
        tree: RuleApplicationTree,
        subtree: TypeDerivationTree,
        discharge: VariableTypeAssertion,
        term: TypedAbstraction
    ) -> TypeDerivationTree:
        # η-reduction
        if isinstance(term.sub, TypedApplication) and term.sub.b == term.var and term.var not in get_free_variables(term.sub.a):
            assert isinstance(subtree, RuleApplicationTree)

            try:
                return alpha_convert_derivation(subtree.premises[0].tree, self.reduct)
            except TypeDerivationError:
                pass

        # Recursion
        if isinstance(self.reduct, TypedAbstraction) and term.var_type == self.reduct.var_type:
            assertion = VariableTypeAssertion(self.reduct.var, self.reduct.var_type)

            if term.var == self.reduct.var:
                adjusted_subtree = subtree
            else:
                if self.reduct.var in get_free_variables(term.sub):
                    raise NotReducible

                adjusted_subtree = substitute(
                    subtree,
                    {term.var: assume(assertion)}
                )

            return apply(
                BASE_EXPLICIT_TYPE_SYSTEM, '→₊',
                premise(
                    discharge=assertion,
                    tree=ReductionVisitor(self.reduct.sub).visit(adjusted_subtree)
                )
            )

        raise NotReducible


# This is alg:simply_typed_reduction in the monograph
def reduce_derivation(tree: TypeDerivationTree, reduct: TypedTerm) -> TypeDerivationTree:
    try:
        return ReductionVisitor(reduct).visit(tree)
    except NotReducible:
        raise TypeDerivationError(f'The term {tree.conclusion.term} is not βη-reducible to {reduct} in one step') from None
