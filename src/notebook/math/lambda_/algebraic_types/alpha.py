from dataclasses import dataclass
from typing import override

from ....support.schemas import SchemaInferenceError
from ..assertions import VariableTypeAssertion
from ..instantiation import AtomicLambdaSchemaInstantiation, infer_instantiation_from_term, instantiate_term_schema
from ..signature import ConstantTermSymbol
from ..terms import Constant, TypedAbstraction, TypedApplication, TypedTerm
from ..type_derivation import (
    AssumptionTree,
    RuleApplicationPremise,
    RuleApplicationTree,
    TypeDerivationError,
    TypeDerivationTree,
    apply,
    assume,
    premise,
)
from ..variables import get_free_variables
from .substitution import substitute_in_tree
from .visitor import SimpleAlgebraicDerivationTreeVisitor


class NotAlphaEquivalent(BaseException):
    pass


@dataclass
class AlphaConversionVisitor(SimpleAlgebraicDerivationTreeVisitor[TypeDerivationTree]):
    other: TypedTerm

    @override
    def visit_assumption(self, tree: AssumptionTree) -> TypeDerivationTree:
        if tree.conclusion.term != self.other:
            raise NotAlphaEquivalent

        return tree

    @override
    def visit_rule_application(self, tree: RuleApplicationTree) -> RuleApplicationTree:
        new_instantiation = AtomicLambdaSchemaInstantiation(type_mapping=tree.instantiation.type_mapping)
        rule = tree.rule

        try:
            new_instantiation |= infer_instantiation_from_term(rule.conclusion.term, self.other)
        except SchemaInferenceError as err:
            raise NotAlphaEquivalent from err

        return apply(
            rule,
            *(
                alpha_convert_derivation_unsafe(
                    application_premise.tree,
                    instantiate_term_schema(rule_premise.main.term, new_instantiation)
                )
                for application_premise, rule_premise in zip(tree.premises, rule.premises, strict=True)
            ),
            instantiation=new_instantiation
        )

    def _visit_abstractor_premise(self, body_tree: TypeDerivationTree, assertion: VariableTypeAssertion, other: TypedTerm) -> RuleApplicationPremise:
        abstraction = TypedAbstraction(assertion.term, assertion.type, body_tree.conclusion.term)

        if not isinstance(other, TypedAbstraction) or abstraction.var_type != other.var_type:
            raise NotAlphaEquivalent

        assertion = VariableTypeAssertion(other.var, abstraction.var_type)

        if abstraction.var == other.var:
            adjusted_subtree = body_tree
        else:
            if other.var in get_free_variables(abstraction.body):
                raise NotAlphaEquivalent

            adjusted_subtree = substitute_in_tree(
                body_tree,
                {abstraction.var: assume(assertion)}
            )

        return premise(
            discharge=assertion,
            tree=alpha_convert_derivation_unsafe(adjusted_subtree, other.body)
        )

    @override
    def visit_arrow_intro(
        self,
        tree: RuleApplicationTree,
        subtree: TypeDerivationTree,
        subtree_discharge: VariableTypeAssertion,
    ) -> RuleApplicationTree:
        new_premise = self._visit_abstractor_premise(subtree, subtree_discharge, self.other)

        # Unlike in the monograph, here we infer the instantiation needed to apply the rule
        return apply(
            tree.rule,
            new_premise
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
        if not isinstance(self.other, TypedApplication) or \
            not isinstance(self.other.left, TypedApplication) or \
            not isinstance(self.other.left.left, TypedApplication) or \
            self.other.left.left.left != Constant(ConstantTermSymbol('S₋')):
            raise NotAlphaEquivalent

        other_sum_term = self.other.right
        other_right_term = self.other.left.right
        other_left_term = self.other.left.left.right

        new_left_premise = self._visit_abstractor_premise(left_subtree, left_subtree_discharge, other_left_term)
        new_right_premise = self._visit_abstractor_premise(right_subtree, right_subtree_discharge, other_right_term)

        # Unlike in the monograph, here we infer the instantiation needed to apply the rule
        return apply(
            tree.rule,
            premise(tree=alpha_convert_derivation_unsafe(sum_subtree, other_sum_term)),
            new_left_premise,
            new_right_premise,
        )

def alpha_convert_derivation_unsafe(tree: TypeDerivationTree, other: TypedTerm) -> TypeDerivationTree:
    return AlphaConversionVisitor(other).visit(tree)


# This is alg:simply_typed_reduction in the monograph
def alpha_convert_derivation(tree: TypeDerivationTree, other: TypedTerm) -> TypeDerivationTree:
    try:
        return alpha_convert_derivation_unsafe(tree, other)
    except NotAlphaEquivalent:
        raise TypeDerivationError(f'The terms {tree.conclusion.term} and {other} are not α-equivalent') from None
