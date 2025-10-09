from collections.abc import Collection, Iterable, Mapping, Sequence
from dataclasses import dataclass
from typing import override

from ....support.inference import AssumptionRenderer, InferenceTree, InferenceTreeRenderer, RuleApplicationRenderer
from ..formulas import Formula, FormulaSubstitutionSpec
from ..instantiation import (
    FormalLogicSchemaInstantiation,
    infer_instantiation_from_formula_substitution_spec,
    infer_instantiation_from_term_substitution_spec,
    instantiate_substitution_spec,
    merge_instantiations,
)
from ..substitution import evaluate_substitution_spec
from ..terms import EigenvariableSchemaSubstitutionSpec, TermSubstitutionSpec, Variable
from ..variables import get_free_variables
from .exceptions import RuleApplicationError
from .markers import Marker
from .system import NaturalDeductionPremise, NaturalDeductionRule


@dataclass(frozen=True)
class AssumptionTree(InferenceTree[FormulaSubstitutionSpec, Mapping[Marker, Formula]]):
    conclusion: FormulaSubstitutionSpec
    marker: Marker

    @override
    def get_assumption_map(self) -> Mapping[Marker, Formula]:
        return {self.marker: self.conclusion.formula}

    @override
    def build_renderer(self, *, conclusion: FormulaSubstitutionSpec | None = None) -> AssumptionRenderer:
        if conclusion is None:
            conclusion = self.conclusion

        return AssumptionRenderer(
            str(conclusion.formula),
            marker=str(self.marker),
            suffix=str(conclusion.sub) if conclusion.sub else None
        )

    def get_free_variables(self) -> Collection[Variable]:
        return get_free_variables(evaluate_substitution_spec(self.conclusion))

    def __str__(self) -> str:
        return self.build_renderer().render()


def assume(assumption: Formula | FormulaSubstitutionSpec, marker: Marker) -> AssumptionTree:
    return AssumptionTree(
        assumption if isinstance(assumption, FormulaSubstitutionSpec) else FormulaSubstitutionSpec(assumption),
        marker
    )


@dataclass(frozen=True)
class RuleApplicationPremise:
    tree: 'ProofTree'
    main: FormulaSubstitutionSpec
    discharge: FormulaSubstitutionSpec | None = None
    marker: Marker | None = None

    def build_renderer(self) -> InferenceTreeRenderer:
        return self.tree.build_renderer(conclusion=self.main)


def premise(
    *,
    tree: 'ProofTree',
    main: Formula | FormulaSubstitutionSpec | None = None,
    main_sub: TermSubstitutionSpec | None = None,
    discharge: Formula | FormulaSubstitutionSpec | None = None,
    discharge_sub: TermSubstitutionSpec | None = None,
    marker: Marker | None = None,
) -> RuleApplicationPremise:
    main_spec: FormulaSubstitutionSpec
    discharge_spec: FormulaSubstitutionSpec | None = None

    if isinstance(main, FormulaSubstitutionSpec):
        if main_sub:
            raise RuleApplicationError(f'Redundant substitution specified for {main}')

        main_spec = main
    elif main:
        main_spec = FormulaSubstitutionSpec(main, main_sub)
    else:
        main_spec = FormulaSubstitutionSpec(
            evaluate_substitution_spec(tree.conclusion),
            main_sub
        )

    if isinstance(discharge, FormulaSubstitutionSpec):
        if discharge_sub:
            raise RuleApplicationError(f'Redundant substitution specified for {discharge}')

        discharge_spec = discharge
    elif discharge:
        discharge_spec = FormulaSubstitutionSpec(discharge, discharge_sub)

    return RuleApplicationPremise(
        tree,
        main_spec,
        discharge_spec,
        marker,
    )


def get_main_eigenvariable(rule_premise: NaturalDeductionPremise, application_premise: RuleApplicationPremise) -> Variable | None:
    if isinstance(rule_premise.main.sub, EigenvariableSchemaSubstitutionSpec):
        if application_premise.main.sub is None:
            raise RuleApplicationError(f'No substitution specified for {application_premise.main} in eigenvariable rule with conclusion {rule_premise.main}')

        if not isinstance(application_premise.main.sub.dest, Variable):
            raise RuleApplicationError(f'The substitution {application_premise.main.sub} should map to a variable')

        return application_premise.main.sub.dest

    return None


def get_discharge_eigenvariable(rule_premise: NaturalDeductionPremise, application_premise: RuleApplicationPremise) -> Variable | None:
    if rule_premise.discharge is None:
        return None

    if isinstance(rule_premise.discharge.sub, EigenvariableSchemaSubstitutionSpec):
        # This is verified during rule application
        assert application_premise.discharge

        if application_premise.discharge.sub is None:
            raise RuleApplicationError(f'No discharge substitution specified for {application_premise.discharge} in eigenvariable rule with discharge schema {rule_premise.discharge}')

        if not isinstance(application_premise.discharge.sub.dest, Variable):
            raise RuleApplicationError(f'The substitution {application_premise.discharge.sub} should map to a variable')

        return application_premise.discharge.sub.dest

    return None


@dataclass(frozen=True)
class RuleApplicationTree(InferenceTree[FormulaSubstitutionSpec, Mapping[Marker, Formula]]):
    rule: NaturalDeductionRule
    instantiation: FormalLogicSchemaInstantiation
    premises: Sequence[RuleApplicationPremise]
    conclusion: FormulaSubstitutionSpec

    def _filter_assumptions(self, *, discharged_at_current_step: bool) -> Iterable[tuple[Marker, Formula]]:
        for application_premise in self.premises:
            for marker, assumption in application_premise.tree.get_assumption_map().items():
                is_discharged_at_current_step = application_premise.discharge is not None and \
                    evaluate_substitution_spec(application_premise.discharge) == assumption and \
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
            free = application_premise.tree.get_free_variables()

            if (var := get_main_eigenvariable(rule_premise, application_premise)) and var in free:
                yield var

            if (var := get_discharge_eigenvariable(rule_premise, application_premise)) and var in free:
                yield var

    def get_eigenvariable_context(self) -> Iterable[Variable | None]:
        return sorted(set(self._iter_eigenvariables()), key=str)

    @override
    def build_renderer(self, *, conclusion: FormulaSubstitutionSpec | None = None) -> RuleApplicationRenderer:
        if conclusion is None:
            conclusion = self.conclusion

        line = str(conclusion)

        return RuleApplicationRenderer(
            line,
            [str(marker) for marker in self.get_marker_context()] + [f'{var}*' for var in self.get_eigenvariable_context()],
            self.rule.name,
            [premise.build_renderer() for premise in self.premises]
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

            if eigen in get_free_variables(evaluate_substitution_spec(application_premise.tree.conclusion)):
                raise RuleApplicationError(f'The discharge formula eigenvariable {eigen} cannot be free in the conclusion {application_premise.tree.conclusion} of the premise')

            # Update instantiation
            instantiation = merge_instantiations(
                instantiation,
                infer_instantiation_from_formula_substitution_spec(
                    rule_premise.discharge,
                    application_premise.discharge
                )
            )

        instantiation = merge_instantiations(
            instantiation,
            infer_instantiation_from_formula_substitution_spec(
                rule_premise.main,
                application_premise.main,
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
