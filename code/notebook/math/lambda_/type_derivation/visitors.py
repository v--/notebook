from ..assertions import VariableTypeAssertion
from ..terms import TypedAbstraction, TypedApplication
from ..type_system import BASE_EXPLICIT_TYPE_SYSTEM
from .exceptions import UnknownDerivationRuleError
from .tree import AssumptionTree, RuleApplicationTree, TypeDerivationTree


class BasicDerivationTreeVisitor[T]:
    def visit(self, tree: TypeDerivationTree) -> T:
        if isinstance(tree, AssumptionTree):
            return self.visit_assumption(tree)

        if isinstance(tree, RuleApplicationTree):
            if tree.get_rule() == BASE_EXPLICIT_TYPE_SYSTEM['→₋']:
                term = tree.conclusion.term
                assert isinstance(term, TypedApplication)
                return self.visit_arrow_elim(tree, tree.premises[0].tree, tree.premises[1].tree, term)

            if tree.get_rule() == BASE_EXPLICIT_TYPE_SYSTEM['→₊']:
                term = tree.conclusion.term
                discharge = tree.premises[0].discharge
                assert isinstance(term, TypedAbstraction)
                assert discharge is not None
                return self.visit_arrow_intro(tree, tree.premises[0].tree, discharge, term)

            raise UnknownDerivationRuleError(f'Unknown rule {tree.rule_name}')

        raise UnknownDerivationRuleError(f'Unknown tree type {type(tree).__name__}')

    def visit_assumption(self, tree: AssumptionTree) -> T:
        return self.generic_visit(tree)

    def visit_arrow_elim(
        self,
        tree: RuleApplicationTree,
        subtree_left: TypeDerivationTree,  # noqa: ARG002
        subtree_right: TypeDerivationTree,  # noqa: ARG002
        term: TypedApplication  # noqa: ARG002
    ) -> T:
        return self.generic_visit(tree)

    def visit_arrow_intro(
        self,
        tree: RuleApplicationTree,
        subtree: TypeDerivationTree,  # noqa: ARG002
        discharge: VariableTypeAssertion,  # noqa: ARG002
        term: TypedAbstraction  # noqa: ARG002
    ) -> T:
        return self.generic_visit(tree)

    def generic_visit(self, tree: TypeDerivationTree) -> T:
        raise NotImplementedError

