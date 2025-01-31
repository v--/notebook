from collections.abc import Collection, Iterable, Sequence
from typing import NamedTuple, Protocol, override

from ....support.inference.rendering import AssumptionRenderer, InferenceTreeRenderer, RuleApplicationRenderer
from ..assertions import TypeAssertion
from ..instantiation import (
    LambdaSchemaInstantiation,
    infer_instantiation_from_assertion,
    instantiate_assertion_schema,
    merge_instantiations,
)
from ..typing_rules import TypingRule
from .exceptions import TypeDerivationError


class TypeDerivationTree(Protocol):
    conclusion: TypeAssertion

    def get_context(self) -> Collection[TypeAssertion]:
        ...

    def build_renderer(self) -> InferenceTreeRenderer:
        ...


class AssumptionTree(TypeDerivationTree):
    conclusion: TypeAssertion

    def __init__(self, assumption: TypeAssertion) -> None:
        self.conclusion = assumption

    @override
    def get_context(self) -> Collection[TypeAssertion]:
        return {self.conclusion}

    @override
    def build_renderer(self) -> AssumptionRenderer:
        return AssumptionRenderer(str(self.conclusion))

    def __str__(self) -> str:
        return self.build_renderer().render()


def assume(assertion: TypeAssertion) -> AssumptionTree:
    return AssumptionTree(assertion)


class RuleApplicationPremise(NamedTuple):
    tree: TypeDerivationTree
    discharge: TypeAssertion | None


class RuleApplicationTree(TypeDerivationTree):
    conclusion: TypeAssertion
    rule: TypingRule
    instantiation: LambdaSchemaInstantiation
    premises: Sequence[RuleApplicationPremise]

    def __init__(
        self,
        rule: TypingRule,
        instantiation: LambdaSchemaInstantiation,
        premises: Sequence[RuleApplicationPremise]
    ) -> None:
        self.conclusion = instantiate_assertion_schema(rule.conclusion, instantiation)
        self.rule = rule
        self.instantiation = instantiation
        self.premises = premises

    def _filter_assumptions(self, *, closed_at_current_step: bool) -> Iterable[TypeAssertion]:
        for rule_premise, application_premise in zip(self.rule.premises, self.premises, strict=True):
            if rule_premise is None:
                continue

            for assumption in application_premise.tree.get_context():
                is_closed_at_current_step = application_premise.discharge == assumption

                if closed_at_current_step == is_closed_at_current_step:
                    yield assumption

    @override
    def get_context(self) -> Collection[TypeAssertion]:
        return set(self._filter_assumptions(closed_at_current_step=False))

    def get_marker_context(self) -> Iterable[TypeAssertion]:
        return sorted(
            set(self._filter_assumptions(closed_at_current_step=True)),
            key=str
        )

    @override
    def build_renderer(self) -> RuleApplicationRenderer:
        return RuleApplicationRenderer(
            str(self.conclusion),
            [f'({assumption})' for assumption in self.get_marker_context()],
            self.rule.name,
            [premise.tree.build_renderer() for premise in self.premises]
        )

    def __str__(self) -> str:
        return self.build_renderer().render()


def apply(rule: TypingRule, *premises: RuleApplicationPremise) -> RuleApplicationTree:
    if len(premises) != len(rule.premises):
        raise TypeDerivationError(f'The rule {rule.name} has {len(rule.premises)} premises, but the application has {len(premises)}')

    instantiation = LambdaSchemaInstantiation()

    for i, (rule_premise, (subtree, discharge)) in enumerate(zip(rule.premises, premises, strict=True), start=1):
        if rule_premise.discharge is not None:
            if discharge is None:
                raise TypeDerivationError(f'The rule {rule.name} requires a discharge type assertion for premise number {i}')

            instantiation = merge_instantiations(instantiation, infer_instantiation_from_assertion(rule_premise.discharge, discharge))

        instantiation = merge_instantiations(instantiation, infer_instantiation_from_assertion(rule_premise.main, subtree.conclusion))

    return RuleApplicationTree(
        rule=rule,
        premises=premises,
        instantiation=instantiation
    )
