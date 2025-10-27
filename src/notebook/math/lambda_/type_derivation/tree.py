from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from typing import override

from ....support.inference import AssumptionRenderer, InferenceTree, RuleApplicationRenderer
from ..assertions import TypeAssertion, VariableTypeAssertion
from ..instantiation import (
    LambdaSchemaInstantiation,
    infer_instantiation_from_assertion,
    instantiate_assertion_schema,
)
from ..terms import Variable
from ..type_system import TypingRule
from ..types import SimpleType
from .exceptions import TypeDerivationError


@dataclass(frozen=True)
class AssumptionTree(InferenceTree[VariableTypeAssertion, Mapping[Variable, SimpleType]]):
    conclusion: VariableTypeAssertion

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TypeDerivationTree):
            return NotImplemented

        return self.conclusion == other.conclusion

    def __hash__(self) -> int:
        return hash(self.conclusion)

    @override
    def get_assumption_map(self) -> Mapping[Variable, SimpleType]:
        return {self.conclusion.term: self.conclusion.type}

    @override
    def build_renderer(self) -> AssumptionRenderer:
        return AssumptionRenderer(str(self.conclusion))

    def __str__(self) -> str:
        return self.build_renderer().render()


def assume(assertion: VariableTypeAssertion) -> AssumptionTree:
    return AssumptionTree(assertion)


@dataclass(frozen=True)
class RuleApplicationPremise:
    tree: TypeDerivationTree
    discharge: VariableTypeAssertion | None = None


def premise(*, tree: TypeDerivationTree, discharge: VariableTypeAssertion | None = None) -> RuleApplicationPremise:
    return RuleApplicationPremise(tree, discharge)


@dataclass(frozen=True)
class RuleApplicationTree(InferenceTree[TypeAssertion, Mapping[Variable, SimpleType]]):
    rule: TypingRule
    instantiation: LambdaSchemaInstantiation
    premises: Sequence[RuleApplicationPremise]
    conclusion: TypeAssertion

    def _filter_assumptions(self, *, discharged_at_current_step: bool) -> Iterable[tuple[Variable, SimpleType]]:
        for application_premise in self.premises:
            for var, type_ in application_premise.tree.get_assumption_map().items():
                is_discharged_at_current_step = application_premise.discharge is not None and \
                    application_premise.discharge.term == var and application_premise.discharge.type == type_

                if discharged_at_current_step == is_discharged_at_current_step:
                    yield var, type_

    @override
    def get_assumption_map(self) -> Mapping[Variable, SimpleType]:
        return dict(self._filter_assumptions(discharged_at_current_step=False))

    def get_marker_context(self) -> Iterable[Variable]:
        return sorted(
            {var for var, type_ in self._filter_assumptions(discharged_at_current_step=True)},
            key=str
        )

    @override
    def build_renderer(self) -> RuleApplicationRenderer:
        return RuleApplicationRenderer(
            str(self.conclusion),
            list(map(str, self.get_marker_context())),
            self.rule.name,
            [premise.tree.build_renderer() for premise in self.premises]
        )

    def __str__(self) -> str:
        return self.build_renderer().render()


def apply(
    rule: TypingRule,
    *args: TypeDerivationTree | RuleApplicationPremise,
    instantiation: LambdaSchemaInstantiation | None = None,
) -> RuleApplicationTree:
    if len(args) != len(rule.premises):
        raise TypeDerivationError(f'The rule {rule.name} has {len(rule.premises)} premises, but the application has {len(args)}')

    instantiation = instantiation or LambdaSchemaInstantiation()
    application_premises = [
        premise(tree=premise_arg) if isinstance(premise_arg, TypeDerivationTree) else premise_arg
        for premise_arg in args
    ]

    for i, (rule_premise, application_premise) in enumerate(zip(rule.premises, application_premises, strict=True), start=1):
        if rule_premise.discharge is not None:
            if application_premise.discharge is None:
                raise TypeDerivationError(f'The rule {rule.name} requires a discharge type assertion for premise number {i}')

            instantiation |= infer_instantiation_from_assertion(rule_premise.discharge, application_premise.discharge)

        instantiation |= infer_instantiation_from_assertion(rule_premise.main, application_premise.tree.conclusion)

    return RuleApplicationTree(
        rule,
        instantiation,
        application_premises,
        instantiate_assertion_schema(rule.conclusion, instantiation)
    )


TypeDerivationTree = AssumptionTree | RuleApplicationTree
