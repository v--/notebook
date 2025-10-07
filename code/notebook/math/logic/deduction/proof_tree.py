from collections.abc import Collection, Iterable, Mapping, Sequence
from dataclasses import dataclass
from typing import override

from ....support.inference import AssumptionRenderer, InferenceTree, RuleApplicationRenderer
from ..formulas import Formula, FormulaSubstitutionSpec
from ..instantiation import (
    FormalLogicSchemaInstantiation,
    infer_instantiation_from_formula_substitution_spec,
    infer_instantiation_from_term_substitution_spec,
    instantiate_substitution_spec,
    merge_instantiations,
)
from ..terms import EigenvariableSchemaSubstitutionSpec, TermSubstitutionSpec, Variable
from ..variables import get_free_variables
from .exceptions import RuleApplicationError
from .markers import Marker
from .system import NaturalDeductionPremise, NaturalDeductionRule


@dataclass(frozen=True)
class AssumptionTree(InferenceTree[Formula, Mapping[Marker, Formula]]):
    conclusion: Formula
    marker: Marker

    @override
    def get_assumption_map(self) -> Mapping[Marker, Formula]:
        return {self.marker: self.conclusion}

    @override
    def build_renderer(self) -> AssumptionRenderer:
        return AssumptionRenderer(str(self.conclusion), marker=str(self.marker))

    def get_free_variables(self) -> Collection[Variable]:
        return get_free_variables(self.conclusion)

    def __str__(self) -> str:
        return self.build_renderer().render()


def assume(assumption: Formula, marker: Marker) -> AssumptionTree:
    return AssumptionTree(assumption, marker)


@dataclass(frozen=True)
class RuleApplicationPremise:
    tree: 'ProofTree'
    main_unsubstituted: Formula
    main_sub: TermSubstitutionSpec | None = None
    discharge: Formula | None = None
    discharge_sub: TermSubstitutionSpec | None = None
    marker: Marker | None = None


def premise(
    *,
    tree: 'ProofTree',
    main_unsubstituted: Formula | None = None,
    main_sub: TermSubstitutionSpec | None = None,
    discharge: Formula | None = None,
    discharge_sub: TermSubstitutionSpec | None = None,
    marker: Marker | None = None,
) -> RuleApplicationPremise:
    return RuleApplicationPremise(
        tree,
        main_unsubstituted or tree.conclusion,
        main_sub,
        discharge,
        discharge_sub,
        marker,
    )


def get_main_eigenvariable(rule_premise: NaturalDeductionPremise, application_premise: RuleApplicationPremise) -> Variable | None:
    if isinstance(rule_premise.main.sub, EigenvariableSchemaSubstitutionSpec):
        if application_premise.main_sub is None:
            raise RuleApplicationError(f'No substitution specified on {application_premise.main_unsubstituted} for eigenvariable rule {rule_premise.main}')

        if not isinstance(application_premise.main_sub.dest, Variable):
            raise RuleApplicationError(f'The substitution {application_premise.main_sub} should map to a variable')

        return application_premise.main_sub.dest

    return None


def get_discharge_eigenvariable(rule_premise: NaturalDeductionPremise, application_premise: RuleApplicationPremise) -> Variable | None:
    if rule_premise.discharge is None:
        return None

    if isinstance(rule_premise.discharge.sub, EigenvariableSchemaSubstitutionSpec):
        if application_premise.discharge_sub is None:
            raise RuleApplicationError(f'No substitution specified on {application_premise.main_unsubstituted} for eigenvariable rule {rule_premise.main}')

        if not isinstance(application_premise.discharge_sub.dest, Variable):
            raise RuleApplicationError(f'The substitution {application_premise.main_sub} should map to a variable')

        return application_premise.discharge_sub.dest

    return None


@dataclass(frozen=True)
class RuleApplicationTree(InferenceTree[Formula, Mapping[Marker, Formula]]):
    rule: NaturalDeductionRule
    instantiation: FormalLogicSchemaInstantiation
    premises: Sequence[RuleApplicationPremise]
    conclusion: Formula

    def _filter_assumptions(self, *, discharged_at_current_step: bool) -> Iterable[tuple[Marker, Formula]]:
        for application_premise in self.premises:
            for marker, assumption in application_premise.tree.get_assumption_map().items():
                is_discharged_at_current_step = application_premise.discharge == assumption and \
                    (application_premise.marker is None or application_premise.marker == marker)

                if discharged_at_current_step == is_discharged_at_current_step:
                    yield marker, assumption

    @override
    def get_assumption_map(self) -> Mapping[Marker, Formula]:
        return dict(self._filter_assumptions(discharged_at_current_step=False))

    def get_marker_context(self) -> Iterable[Marker]:
        return sorted(
            (marker for marker, formula in self._filter_assumptions(discharged_at_current_step=True)),
            key=str
        )

    def _iter_eigenvariables(self) -> Iterable[Variable]:
        for rule_premise, application_premise in zip(self.rule.premises, self.premises, strict=True):
            if var := get_main_eigenvariable(rule_premise, application_premise):
                yield var

            if var := get_discharge_eigenvariable(rule_premise, application_premise):
                yield var

    def get_eigenvariable_context(self) -> Iterable[Variable | None]:
        return sorted(set(self._iter_eigenvariables()), key=str)

    @override
    def build_renderer(self) -> RuleApplicationRenderer:
        return RuleApplicationRenderer(
            str(self.conclusion),
            [str(marker) for marker in self.get_marker_context()] + [f'{var}*' for var in self.get_eigenvariable_context()],
            self.rule.name,
            [premise.tree.build_renderer() for premise in self.premises]
        )

    def iter_free_variables(self) -> Iterable[Variable]:
        for rule_premise, application_premise in zip(self.rule.premises, self.premises, strict=True):
            if application_premise.discharge:
                continue

            eigen = get_main_eigenvariable(rule_premise, application_premise)

            for var in application_premise.tree.get_free_variables():
                if var != eigen:
                    yield var

    def get_free_variables(self) -> Collection[Variable]:
        return set(self.iter_free_variables())

    def __str__(self) -> str:
        return self.build_renderer().render()


def apply(
    rule: NaturalDeductionRule,
    *args: 'ProofTree | RuleApplicationPremise',
    instantiation: FormalLogicSchemaInstantiation | None = None,
    conclusion_sub: TermSubstitutionSpec | None = None,
) -> RuleApplicationTree:
    if len(args) != len(rule.premises):
        raise RuleApplicationError(f'The rule {rule.name} has {len(rule.premises)} premises, but the application has {len(args)}')

    instantiation = instantiation or FormalLogicSchemaInstantiation()
    marker_map = dict[Marker, Formula]()

    application_premises = [
        premise(tree=premise_arg) if isinstance(premise_arg, ProofTree) else premise_arg
        for premise_arg in args
    ]

    for i, (rule_premise, application_premise) in enumerate(zip(rule.premises, application_premises, strict=True), start=1):
        for marker, assumption in application_premise.tree.get_assumption_map().items():
            if marker in marker_map and marker_map[marker] != assumption:
                raise RuleApplicationError('Multiple assumptions cannot have the same marker')

            marker_map[marker] = assumption

        # Check if there is an eigenvariable in the main formula
        eigen = get_main_eigenvariable(rule_premise, application_premise)

        if eigen in application_premise.tree.get_free_variables():
            raise RuleApplicationError(f'The eigenvariable {eigen} cannot be free in the derivation of {application_premise.tree.conclusion}')

        if rule_premise.discharge:
            if application_premise.discharge is None:
                raise RuleApplicationError(f'The rule {rule.name} requires a discharge formula for premise number {i}')

            # Check if there is an eigenvariable in the discharge formula
            eigen = get_discharge_eigenvariable(rule_premise, application_premise)

            if eigen in application_premise.tree.get_free_variables():
                raise RuleApplicationError(f'The discharge formula eigenvariable {eigen} cannot be free in the derivation of {application_premise.discharge}')

            if eigen in get_free_variables(application_premise.tree.conclusion):
                raise RuleApplicationError(f'The discharge formula eigenvariable {eigen} cannot be free in the conclusion {application_premise.tree.conclusion} of the premise')

            # Update instantiation
            instantiation = merge_instantiations(
                instantiation,
                infer_instantiation_from_formula_substitution_spec(
                    rule_premise.discharge,
                    FormulaSubstitutionSpec(
                        application_premise.discharge,
                        application_premise.discharge_sub
                    )
                )
            )

        instantiation = merge_instantiations(
            instantiation,
            infer_instantiation_from_formula_substitution_spec(
                rule_premise.main,
                FormulaSubstitutionSpec(
                    application_premise.main_unsubstituted,
                    application_premise.main_sub,
                )
            )
        )

    if rule.conclusion.sub:
        if not conclusion_sub:
            raise RuleApplicationError('Expected a substitution of the conclusion')

        instantiation = merge_instantiations(
            instantiation,
            infer_instantiation_from_term_substitution_spec(rule.conclusion.sub, conclusion_sub)
        )

    return RuleApplicationTree(
        rule,
        instantiation,
        application_premises,
        instantiate_substitution_spec(rule.conclusion, instantiation)
    )


ProofTree = AssumptionTree | RuleApplicationTree
