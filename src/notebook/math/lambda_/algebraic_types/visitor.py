# ruff: noqa: ARG002

from ..assertions import VariableTypeAssertion
from ..type_derivation import AssumptionTree, RuleApplicationTree, TypeDerivationTree, UnknownDerivationRuleError
from ..types import SimpleType
from .system import SIMPLE_ALGEBRAIC_TYPE_SYSTEM


class SimpleAlgebraicDerivationTreeVisitor[T]:
    def visit(self, tree: TypeDerivationTree) -> T:  # noqa: PLR0911
        if isinstance(tree, AssumptionTree):
            return self.visit_assumption(tree)

        if tree.rule == SIMPLE_ALGEBRAIC_TYPE_SYSTEM['→₊']:
            discharge = tree.premises[0].attachments[0]
            assert discharge is not None
            return self.visit_arrow_intro(
                tree=tree,
                subtree=tree.premises[0].tree,
                subtree_discharge=discharge,
            )

        if tree.rule == SIMPLE_ALGEBRAIC_TYPE_SYSTEM['→₋']:
                return self.visit_arrow_elim(
                    tree=tree,
                    subtree_left=tree.premises[0].tree,
                    subtree_right=tree.premises[1].tree
                )

        if tree.rule == SIMPLE_ALGEBRAIC_TYPE_SYSTEM['𝟘₋']:
            return self.visit_empty_elim(
                tree=tree,
                subtree=tree.premises[0].tree,
                new_type=tree.conclusion.type
            )

        if tree.rule == SIMPLE_ALGEBRAIC_TYPE_SYSTEM['𝟙₊']:
            return self.visit_unit_intro(tree)

        if tree.rule == SIMPLE_ALGEBRAIC_TYPE_SYSTEM['×₊']:
            return self.visit_prod_intro(
                tree=tree,
                left_subtree=tree.premises[0].tree,
                right_subtree=tree.premises[1].tree
            )

        if tree.rule == SIMPLE_ALGEBRAIC_TYPE_SYSTEM['×₋ₗ']:
            return self.visit_prod_elim_left(
                tree=tree,
                subtree=tree.premises[0].tree
            )

        if tree.rule == SIMPLE_ALGEBRAIC_TYPE_SYSTEM['×₋ᵣ']:
            return self.visit_prod_elim_right(
                tree=tree,
                subtree=tree.premises[1].tree
            )

        if tree.rule == SIMPLE_ALGEBRAIC_TYPE_SYSTEM['+₊ₗ']:
            return self.visit_sum_intro_left(
                tree=tree,
                subtree=tree.premises[0].tree
            )

        if tree.rule == SIMPLE_ALGEBRAIC_TYPE_SYSTEM['+₊ᵣ']:
            return self.visit_sum_intro_left(
                tree=tree,
                subtree=tree.premises[1].tree
            )

        if tree.rule == SIMPLE_ALGEBRAIC_TYPE_SYSTEM['+₋']:
            left_discharge = tree.premises[1].attachments[0]
            assert left_discharge is not None

            right_discharge = tree.premises[2].attachments[0]
            assert right_discharge is not None

            return self.visit_sum_elim(
                tree=tree,
                sum_subtree=tree.premises[0].tree,
                left_subtree=tree.premises[1].tree,
                left_subtree_discharge=left_discharge,
                right_subtree=tree.premises[2].tree,
                right_subtree_discharge=right_discharge,
            )

        raise UnknownDerivationRuleError(tree.rule)

    def visit_assumption(self, tree: AssumptionTree) -> T:
        return self.generic_visit(tree)

    def visit_arrow_intro(
        self,
        tree: RuleApplicationTree,
        subtree: TypeDerivationTree,
        subtree_discharge: VariableTypeAssertion,
    ) -> T:
        return self.visit_rule_application(tree)

    def visit_arrow_elim(
        self,
        tree: RuleApplicationTree,
        subtree_left: TypeDerivationTree,
        subtree_right: TypeDerivationTree,
    ) -> T:
        return self.visit_rule_application(tree)

    def visit_empty_elim(
        self,
        tree: RuleApplicationTree,
        subtree: TypeDerivationTree,
        new_type: SimpleType,
    ) -> T:
        return self.visit_rule_application(tree)

    def visit_unit_intro(
        self,
        tree: RuleApplicationTree,
    ) -> T:
        return self.visit_rule_application(tree)

    def visit_prod_intro(
        self,
        tree: RuleApplicationTree,
        left_subtree: TypeDerivationTree,
        right_subtree: TypeDerivationTree,
    ) -> T:
        return self.visit_rule_application(tree)

    def visit_prod_elim_left(
        self,
        tree: RuleApplicationTree,
        subtree: TypeDerivationTree,
    ) -> T:
        return self.visit_rule_application(tree)

    def visit_prod_elim_right(
        self,
        tree: RuleApplicationTree,
        subtree: TypeDerivationTree,
    ) -> T:
        return self.visit_rule_application(tree)

    def visit_sum_intro_left(
        self,
        tree: RuleApplicationTree,
        subtree: TypeDerivationTree,
    ) -> T:
        return self.visit_rule_application(tree)

    def visit_sum_intro_right(
        self,
        tree: RuleApplicationTree,
        subtree: TypeDerivationTree,
    ) -> T:
        return self.visit_rule_application(tree)

    def visit_sum_elim(
        self,
        tree: RuleApplicationTree,
        sum_subtree: TypeDerivationTree,
        left_subtree: TypeDerivationTree,
        left_subtree_discharge: VariableTypeAssertion,
        right_subtree: TypeDerivationTree,
        right_subtree_discharge: VariableTypeAssertion,
    ) -> T:
        return self.visit_rule_application(tree)

    def visit_rule_application(self, tree: RuleApplicationTree) -> T:
        return self.generic_visit(tree)

    def generic_visit(self, tree: TypeDerivationTree) -> T:
        raise NotImplementedError

