from collections.abc import Collection, Iterable, Mapping, Sequence
from dataclasses import dataclass
from typing import override

from ....support.inference import AssumptionRenderer, InferenceTree, RuleApplicationRenderer
from ....support.schemas import SchemaInstantiationError
from ..assertions import TypeAssertion, VariableTypeAssertion
from ..instantiation import (
    AtomicLambdaSchemaInstantiation,
    infer_instantiation_from_assertion,
    instantiate_assertion_schema,
)
from ..terms import Variable, VariablePlaceholder
from ..type_system import TypingRule
from ..types import SimpleType, TypePlaceholder
from .exceptions import TypeDerivationError


@dataclass(frozen=True)
class AssumptionTree(InferenceTree[VariableTypeAssertion, VariableTypeAssertion]):
    conclusion: VariableTypeAssertion

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TypeDerivationTree):
            return NotImplemented

        return self.conclusion == other.conclusion

    def __hash__(self) -> int:
        return hash(self.conclusion)

    @override
    def get_cumulative_assumptions(self) -> Collection[VariableTypeAssertion]:
        return {self.conclusion}

    @override
    def build_renderer(self) -> AssumptionRenderer:
        return AssumptionRenderer(str(self.conclusion))

    def __str__(self) -> str:
        return self.build_renderer().render()


def assume(assertion: VariableTypeAssertion) -> AssumptionTree:
    return AssumptionTree(assertion)


# Unlike in logic, we do not need a distinct RuleApplicationPremiseConfig class
@dataclass(frozen=True)
class RuleApplicationPremise:
    tree: TypeDerivationTree
    attachments: Sequence[VariableTypeAssertion | None]


def premise_config(
    *,
    tree: TypeDerivationTree,
    attachments: Sequence[VariableTypeAssertion | None] = []
) -> RuleApplicationPremise:
    return RuleApplicationPremise(tree, attachments)


@dataclass(frozen=True)
class RuleApplicationTree(InferenceTree[TypeAssertion, VariableTypeAssertion]):
    rule: TypingRule
    instantiation: AtomicLambdaSchemaInstantiation
    premises: Sequence[RuleApplicationPremise]
    conclusion: TypeAssertion

    def _filter_assumptions(self, *, discharged_at_current_step: bool) -> Iterable[VariableTypeAssertion]:
        for premise in self.premises:
            for assumption in premise.tree.get_cumulative_assumptions():
                is_discharged_at_current_step = any(
                    att and att.term == assumption.term and att.type == assumption.type
                    for att in premise.attachments
                )

                if discharged_at_current_step == is_discharged_at_current_step:
                    yield assumption

    @override
    def get_cumulative_assumptions(self) -> Collection[VariableTypeAssertion]:
        return set(self._filter_assumptions(discharged_at_current_step=False))

    def get_locally_discharged_markers(self) -> Iterable[Variable]:
        return sorted(
            {assumption.term for assumption in self._filter_assumptions(discharged_at_current_step=True)},
            key=str
        )

    @override
    def build_renderer(self) -> RuleApplicationRenderer:
        return RuleApplicationRenderer(
            str(self.conclusion),
            list(map(str, self.get_locally_discharged_markers())),
            self.rule.name,
            [premise.tree.build_renderer() for premise in self.premises]
        )

    def __str__(self) -> str:
        return self.build_renderer().render()


def apply(
    rule: TypingRule,
    *args: TypeDerivationTree | RuleApplicationPremise,
    instantiation: AtomicLambdaSchemaInstantiation | None = None,
    implicit_variables: Mapping[VariablePlaceholder, Variable] | None = None,
    implicit_types: Mapping[TypePlaceholder, SimpleType] | None = None,
) -> RuleApplicationTree:
    if len(args) != len(rule.premises):
        raise TypeDerivationError(f'The rule {rule.name} has {len(rule.premises)} premises, but the application has {len(args)}')

    if instantiation is None:
        instantiation = AtomicLambdaSchemaInstantiation(variable_mapping=implicit_variables, type_mapping=implicit_types)
    elif implicit_variables or implicit_types:
        raise TypeDerivationError('Cannot provide both an instantiation and implicit variables or types')

    application_premises = [
        premise_config(tree=premise_arg) if isinstance(premise_arg, TypeDerivationTree) else premise_arg
        for premise_arg in args
    ]

    for i, (rule_premise, application_premise) in enumerate(zip(rule.premises, application_premises, strict=True), start=1):
        if len(application_premise.attachments) != len(rule_premise.attachments):
            if len(rule_premise.attachments) == 1:
                raise TypeDerivationError(f'The rule {rule.name} requires an attachments assertion for premise number {i}')

            raise TypeDerivationError(f'The rule {rule.name} requires {len(rule_premise.attachments)} attachments assertions for premise number {i}')

        for attachment_schema, attached in zip(rule_premise.attachments, application_premise.attachments, strict=True):
            if attached:
                instantiation |= infer_instantiation_from_assertion(attachment_schema, attached)

        instantiation |= infer_instantiation_from_assertion(rule_premise.main, application_premise.tree.conclusion)

    for attachment_schema in rule.conclusion.attachments:
        try:
            instantiate_assertion_schema(attachment_schema, instantiation)
        except SchemaInstantiationError as err:
            raise TypeDerivationError(f'Cannot instantiate the implicit premise {attachment_schema} of the rule {rule.name}') from err

    return RuleApplicationTree(
        rule,
        instantiation,
        application_premises,
        instantiate_assertion_schema(rule.conclusion.main, instantiation)
    )


TypeDerivationTree = AssumptionTree | RuleApplicationTree
