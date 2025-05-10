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
from .exceptions import TypeDerivationError
from .substitution import substitute
from .tree import AssumptionTree, RuleApplicationTree, TypeDerivationTree, apply, assume, premise
from .visitors import BasicDerivationTreeVisitor


class NotAlphaEquivalent(BaseException):
    pass


@dataclass
class AlphaConversionVisitor(BasicDerivationTreeVisitor[TypeDerivationTree]):
    other: TypedTerm

    @override
    def visit_assumption(self, tree: AssumptionTree) -> TypeDerivationTree:
        if tree.conclusion.term != self.other:
            raise NotAlphaEquivalent

        return tree

    @override
    def visit_arrow_elim(
        self,
        tree: RuleApplicationTree,
        subtree_left: TypeDerivationTree,
        subtree_right: TypeDerivationTree,
        term: TypedApplication
    ) -> RuleApplicationTree:
        if not isinstance(self.other, TypedApplication):
            raise NotAlphaEquivalent

        return apply(
            BASE_EXPLICIT_TYPE_SYSTEM, '→₋',
            AlphaConversionVisitor(self.other.a).visit(subtree_left),
            AlphaConversionVisitor(self.other.b).visit(subtree_right)
        )

    @override
    def visit_arrow_intro(
        self,
        tree: RuleApplicationTree,
        subtree: TypeDerivationTree,
        discharge: VariableTypeAssertion,
        term: TypedAbstraction
    ) -> RuleApplicationTree:
        if not isinstance(self.other, TypedAbstraction) or term.var_type != self.other.var_type:
            raise NotAlphaEquivalent

        assertion = VariableTypeAssertion(self.other.var, term.var_type)

        if term.var == self.other.var:
            adjusted_subtree = subtree
        else:
            if self.other.var in get_free_variables(term.sub):
                raise NotAlphaEquivalent

            adjusted_subtree = substitute(
                subtree,
                {term.var: assume(assertion)}
            )

        return apply(
            BASE_EXPLICIT_TYPE_SYSTEM, '→₊',
            premise(
                discharge=assertion,
                tree=AlphaConversionVisitor(self.other.sub).visit(adjusted_subtree)
            )
        )

# This is alg:simply_typed_reduction in the monograph
def alpha_convert_derivation(tree: TypeDerivationTree, other: TypedTerm) -> TypeDerivationTree:
    try:
        return AlphaConversionVisitor(other).visit(tree)
    except NotAlphaEquivalent:
        raise TypeDerivationError(f'The terms {tree.conclusion.term} and {other} are not α-equivalent') from None
