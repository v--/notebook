from collections.abc import Collection, Iterable, Sequence
from typing import NamedTuple, Protocol, override

from ....support.inference.rendering import AssumptionRenderer, InferenceTreeRenderer, RuleApplicationRenderer
from ..formulas import Formula
from ..instantiation import (
    FormalLogicSchemaInstantiation,
    infer_instantiation_from_formula,
    instantiate_formula_schema,
    merge_instantiations,
)
from .exceptions import RuleApplicationError
from .markers import MarkedFormula, Marker
from .rules import NaturalDeductionRule


class ProofTree(Protocol):
    conclusion: Formula

    def get_context(self) -> Collection[MarkedFormula]:
        ...

    def build_renderer(self) -> InferenceTreeRenderer:
        ...


class AssumptionTree(ProofTree):
    marked_assumption: MarkedFormula
    conclusion: Formula

    def __init__(self, marked_assumption: MarkedFormula) -> None:
        self.marked_assumption = marked_assumption
        self.conclusion = marked_assumption.formula

    @override
    def get_context(self) -> Collection[MarkedFormula]:
        return {self.marked_assumption}

    @override
    def build_renderer(self) -> AssumptionRenderer:
        return AssumptionRenderer(str(self.conclusion), marker=str(self.marked_assumption.marker))

    def __str__(self) -> str:
        return self.build_renderer().render()


def assume(marked_assumption: MarkedFormula) -> AssumptionTree:
    return AssumptionTree(marked_assumption)


class RuleApplicationPremise(NamedTuple):
    tree: ProofTree
    discharge: Formula | None = None
    marker: Marker | None = None


class RuleApplicationTree(ProofTree):
    conclusion: Formula
    rule: NaturalDeductionRule
    instantiation: FormalLogicSchemaInstantiation
    premises: Sequence[RuleApplicationPremise]

    def __init__(
        self,
        rule: NaturalDeductionRule,
        instantiation: FormalLogicSchemaInstantiation,
        premises: Sequence[RuleApplicationPremise]
    ) -> None:
        self.conclusion = instantiate_formula_schema(rule.conclusion, instantiation)
        self.rule = rule
        self.instantiation = instantiation
        self.premises = premises

    def _filter_assumptions(self, *, discharged_at_current_step: bool) -> Iterable[MarkedFormula]:
        for rule_premise, application_premise in zip(self.rule.premises, self.premises, strict=True):
            if rule_premise is None:
                continue

            for marked_assumption in application_premise.tree.get_context():
                is_discharged_at_current_step = application_premise.discharge == marked_assumption.formula and \
                    (application_premise.marker is None or application_premise.marker == marked_assumption.marker)

                if discharged_at_current_step == is_discharged_at_current_step:
                    yield marked_assumption

    @override
    def get_context(self) -> Collection[MarkedFormula]:
        return set(self._filter_assumptions(discharged_at_current_step=False))

    def get_marker_context(self) -> Iterable[MarkedFormula]:
        return sorted(
            set(self._filter_assumptions(discharged_at_current_step=True)),
            key=str
        )

    @override
    def build_renderer(self) -> RuleApplicationRenderer:
        return RuleApplicationRenderer(
            str(self.conclusion),
            [str(marked_assumption.marker) for marked_assumption in self.get_marker_context()],
            self.rule.name,
            [premise.tree.build_renderer() for premise in self.premises]
        )

    def __str__(self) -> str:
        return self.build_renderer().render()


def apply(rule: NaturalDeductionRule, *premises: RuleApplicationPremise) -> RuleApplicationTree:
    if len(premises) != len(rule.premises):
        raise RuleApplicationError(f'The rule {rule.name} has {len(rule.premises)} premises, but the application has {len(premises)}')

    instantiation = FormalLogicSchemaInstantiation()
    marker_map = dict[Marker, Formula]()

    for i, (rule_premise, (subtree, discharge, _)) in enumerate(zip(rule.premises, premises, strict=True), start=1):
        for assumption, marker in subtree.get_context():
            if marker in marker_map and marker_map[marker] != assumption:
                raise RuleApplicationError('Multiple assumptions cannot have the same marker')

            marker_map[marker] = assumption

        if rule_premise.discharge is not None:
            if discharge is None:
                raise RuleApplicationError(f'The rule {rule.name} requires a discharge formula for premise number {i}')

            instantiation = merge_instantiations(instantiation, infer_instantiation_from_formula(rule_premise.discharge, discharge))

        instantiation = merge_instantiations(instantiation, infer_instantiation_from_formula(rule_premise.main, subtree.conclusion))

    return RuleApplicationTree(
        rule=rule,
        premises=premises,
        instantiation=instantiation
    )
