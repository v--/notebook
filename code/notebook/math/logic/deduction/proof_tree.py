from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from typing import Protocol, override, runtime_checkable

from ....support.inference import AssumptionRenderer, InferenceTreeRenderer, RuleApplicationRenderer
from ..formulas import Formula
from ..instantiation import (
    FormalLogicSchemaInstantiation,
    infer_instantiation_from_formula,
    instantiate_formula_schema,
    merge_instantiations,
)
from .exceptions import RuleApplicationError
from .markers import Marker
from .rules import NaturalDeductionRule
from .system import NaturalDeductionSystem


@runtime_checkable
class ProofTree(Protocol):
    conclusion: Formula

    def get_context(self) -> Mapping[Marker, Formula]:
        ...

    def build_renderer(self) -> InferenceTreeRenderer:
        ...


@dataclass(frozen=True)
class AssumptionTree(ProofTree):
    conclusion: Formula
    marker: Marker

    @override
    def get_context(self) -> Mapping[Marker, Formula]:
        return {self.marker: self.conclusion}

    @override
    def build_renderer(self) -> AssumptionRenderer:
        return AssumptionRenderer(str(self.conclusion), marker=str(self.marker))

    def __str__(self) -> str:
        return self.build_renderer().render()


def assume(assumption: Formula, marker: Marker) -> AssumptionTree:
    return AssumptionTree(assumption, marker)


@dataclass(frozen=True)
class RuleApplicationPremise:
    tree: ProofTree
    discharge: Formula | None = None
    marker: Marker | None = None


def premise(*, tree: ProofTree, discharge: Formula | None = None, marker: Marker | None = None) -> RuleApplicationPremise:
    return RuleApplicationPremise(tree, discharge, marker)


@dataclass(frozen=True)
class RuleApplicationTree(ProofTree):
    system: NaturalDeductionSystem
    rule_name: str
    instantiation: FormalLogicSchemaInstantiation
    premises: Sequence[RuleApplicationPremise]
    conclusion: Formula

    def get_rule(self) -> NaturalDeductionRule:
        return self.system[self.rule_name]

    def _filter_assumptions(self, *, discharged_at_current_step: bool) -> Iterable[tuple[Marker, Formula]]:
        for rule_premise, application_premise in zip(self.get_rule().premises, self.premises, strict=True):
            if rule_premise is None:
                continue

            for marker, assumption in application_premise.tree.get_context().items():
                is_discharged_at_current_step = application_premise.discharge == assumption and \
                    (application_premise.marker is None or application_premise.marker == marker)

                if discharged_at_current_step == is_discharged_at_current_step:
                    yield marker, assumption

    @override
    def get_context(self) -> Mapping[Marker, Formula]:
        return dict(self._filter_assumptions(discharged_at_current_step=False))

    def get_marker_context(self) -> Iterable[Marker]:
        return sorted(
            (marker for marker, formula in self._filter_assumptions(discharged_at_current_step=True)),
            key=str
        )

    @override
    def build_renderer(self) -> RuleApplicationRenderer:
        return RuleApplicationRenderer(
            str(self.conclusion),
            [str(marker) for marker in self.get_marker_context()],
            self.rule_name,
            [premise.tree.build_renderer() for premise in self.premises]
        )

    def __str__(self) -> str:
        return self.build_renderer().render()


def apply(
    system: NaturalDeductionSystem,
    rule_name: str,
    *args: ProofTree | RuleApplicationPremise,
    instantiation: FormalLogicSchemaInstantiation | None = None,
) -> RuleApplicationTree:
    rule = system[rule_name]

    if len(args) != len(rule.premises):
        raise RuleApplicationError(f'The rule {rule_name} has {len(rule.premises)} premises, but the application has {len(args)}')

    instantiation = instantiation or FormalLogicSchemaInstantiation()
    marker_map = dict[Marker, Formula]()

    application_premises = [
        premise(tree=premise_arg) if isinstance(premise_arg, ProofTree) else premise_arg
        for premise_arg in args
    ]

    for i, (rule_premise, application_premise) in enumerate(zip(rule.premises, application_premises, strict=True), start=1):
        for marker, assumption in application_premise.tree.get_context().items():
            if marker in marker_map and marker_map[marker] != assumption:
                raise RuleApplicationError('Multiple assumptions cannot have the same marker')

            marker_map[marker] = assumption

        if rule_premise.discharge is not None:
            if application_premise.discharge is None:
                raise RuleApplicationError(f'The rule {rule_name} requires a discharge formula for premise number {i}')

            instantiation = merge_instantiations(
                instantiation,
                infer_instantiation_from_formula(rule_premise.discharge, application_premise.discharge)
            )

        instantiation = merge_instantiations(
            instantiation,
            infer_instantiation_from_formula(rule_premise.main, application_premise.tree.conclusion)
        )

    return RuleApplicationTree(
        system,
        rule_name,
        instantiation,
        application_premises,
        instantiate_formula_schema(rule.conclusion, instantiation)
    )
