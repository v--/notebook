from collections.abc import Collection, Iterable, Mapping, Sequence
from dataclasses import dataclass
from typing import override

from ....support.inference import (
    AssumptionRenderer,
    InferenceTree,
    InferenceTreeRenderer,
    RuleApplicationRenderer,
)
from ....support.unicode import to_superscript
from ..formulas import Formula, FormulaWithSubstitution
from ..instantiation import (
    FormalLogicSchemaInstantiation,
    infer_instantiation_from_formula_substitution_spec,
    infer_instantiation_from_term_substitution_spec,
    instantiate_substitution_spec,
)
from ..substitution import evaluate_substitution_spec
from ..terms import EigenvariableSchemaSubstitutionSpec, TermSubstitutionSpec, Variable
from ..variables import get_formula_free_variables
from .exceptions import RuleApplicationError
from .markers import Marker
from .system import NaturalDeductionPremise, NaturalDeductionRule


@dataclass(frozen=True)
class MarkedVariable:
    var: Variable
    marker: Marker

    def __str__(self) -> str:
        return f'{self.var}: {self.marker}'


@dataclass(frozen=True)
class AssumptionTree(InferenceTree[FormulaWithSubstitution, Mapping[Marker, Formula]]):
    conclusion: FormulaWithSubstitution
    marker: Marker

    @override
    def get_assumption_map(self) -> Mapping[Marker, Formula]:
        return {self.marker: self.conclusion.formula}

    @override
    def build_renderer(self, *, conclusion: FormulaWithSubstitution | None = None) -> AssumptionRenderer:
        if conclusion is None:
            conclusion = self.conclusion

        return AssumptionRenderer(
            str(conclusion.formula),
            marker=str(self.marker),
            suffix=f'[{conclusion.sub}]' if conclusion.sub and not conclusion.sub.is_noop() else None
        )

    def get_free_variables(self) -> Collection[Variable]:
        return get_formula_free_variables(evaluate_substitution_spec(self.conclusion))

    def get_marked_free_variables(self) -> Collection[MarkedVariable]:
        return {
            MarkedVariable(var, self.marker)
            for var in self.get_free_variables()
        }

    def __str__(self) -> str:
        return self.build_renderer().render()


def assume(assumption: Formula, marker: Marker) -> AssumptionTree:
    return AssumptionTree(
        FormulaWithSubstitution(assumption),
        marker
    )


@dataclass(frozen=True)
class RuleApplicationPremise:
    tree: ProofTree
    main: FormulaWithSubstitution
    discharge: FormulaWithSubstitution | None = None
    marker: Marker | None = None

    def build_renderer(self) -> InferenceTreeRenderer:
        return self.tree.build_renderer(conclusion=self.main)


def premise(
    *,
    tree: ProofTree,
    main: Formula | FormulaWithSubstitution | None = None,
    main_noop_sub: Variable | None = None,
    discharge: Formula | FormulaWithSubstitution | None = None,
    discharge_noop_sub: Variable | None = None,
    marker: Marker | None = None,
) -> RuleApplicationPremise:
    main_spec: FormulaWithSubstitution
    discharge_spec: FormulaWithSubstitution | None = None

    if isinstance(main, FormulaWithSubstitution):
        if main_noop_sub:
            raise RuleApplicationError(f'Redundant substitution specified for {main}')

        main_spec = main
    elif main:
        main_spec = FormulaWithSubstitution(main)
    else:
        main_spec = FormulaWithSubstitution(
            evaluate_substitution_spec(tree.conclusion),
            TermSubstitutionSpec(main_noop_sub, main_noop_sub) if main_noop_sub else None
        )

    if isinstance(discharge, FormulaWithSubstitution):
        if discharge_noop_sub:
            raise RuleApplicationError(f'Redundant substitution specified for {discharge}')

        discharge_spec = discharge
    elif discharge:
        discharge_spec = FormulaWithSubstitution(
            discharge,
            TermSubstitutionSpec(discharge_noop_sub, discharge_noop_sub) if discharge_noop_sub else None
        )

    return RuleApplicationPremise(
        tree,
        main_spec,
        discharge_spec,
        marker,
    )


@dataclass(frozen=True)
class Eigenvariable:
    var: Variable
    formula: Formula
    src: Variable

    def is_renamed(self) -> bool:
        return self.var != self.src

    def __str__(self) -> str:
        return str(self.var)

    def with_star(self) -> str:
        return f'{self.var}*'

    def get_sub(self) -> TermSubstitutionSpec:
        return TermSubstitutionSpec(self.src, self.var)


def get_main_eigenvariable(rule_premise: NaturalDeductionPremise, application_premise: RuleApplicationPremise) -> Eigenvariable | None:
    if isinstance(rule_premise.main.sub, EigenvariableSchemaSubstitutionSpec):
        main_sub = application_premise.main.sub

        if main_sub is None:
            raise RuleApplicationError(f'No substitution specified for {application_premise.main} in eigenvariable rule with conclusion {rule_premise.main}') from None

        if not isinstance(main_sub.dest, Variable):
            raise RuleApplicationError(f'The eigenvariable substitution {main_sub} should map to a variable')

        return Eigenvariable(main_sub.dest, application_premise.main.formula, main_sub.src)

    return None


def get_discharge_eigenvariable(rule_premise: NaturalDeductionPremise, application_premise: RuleApplicationPremise) -> Eigenvariable | None:
    if rule_premise.discharge is None:
        return None

    if isinstance(rule_premise.discharge.sub, EigenvariableSchemaSubstitutionSpec):
        discharge_sub = application_premise.discharge.sub if application_premise.discharge else None

        if discharge_sub is None:
            raise RuleApplicationError(f'No discharge substitution specified for {application_premise.discharge} in eigenvariable rule with discharge schema {rule_premise.discharge}')

        assert application_premise.discharge is not None

        if not isinstance(discharge_sub.dest, Variable):
            raise RuleApplicationError(f'The eigenvariable substitution {discharge_sub} should map to a variable')

        return Eigenvariable(discharge_sub.dest, application_premise.discharge.formula, discharge_sub.src)

    return None


@dataclass(frozen=True)
class RuleApplicationTree(InferenceTree[FormulaWithSubstitution, Mapping[Marker, Formula]]):
    rule: NaturalDeductionRule
    instantiation: FormalLogicSchemaInstantiation
    premises: Sequence[RuleApplicationPremise]
    conclusion: FormulaWithSubstitution

    def _filter_assumptions(self, *, discharged_at_current_step: bool) -> Iterable[tuple[Marker, Formula]]:
        for application_premise in self.premises:
            for marker, assumption in application_premise.tree.get_assumption_map().items():
                is_discharged_at_current_step = application_premise.discharge is not None and \
                    evaluate_substitution_spec(application_premise.discharge) == assumption and \
                    application_premise.marker == marker

                if discharged_at_current_step == is_discharged_at_current_step:
                    yield marker, assumption

    @override
    def get_assumption_map(self) -> Mapping[Marker, Formula]:
        return dict(self._filter_assumptions(discharged_at_current_step=False))

    def get_marker_context(self) -> Iterable[Marker]:
        return sorted(
            {marker for marker, formula in self._filter_assumptions(discharged_at_current_step=True)},
            key=str
        )

    def _iter_dischargeable_eigenvariables(self) -> Iterable[Eigenvariable]:
        for rule_premise, application_premise in zip(self.rule.premises, self.premises, strict=True):
            free = application_premise.tree.get_free_variables()

            if (eigen := get_main_eigenvariable(rule_premise, application_premise)) and eigen.var in free:
                yield eigen

            if (eigen := get_discharge_eigenvariable(rule_premise, application_premise)) and eigen.var in free:
                yield eigen

    def get_eigenvariable_context(self) -> Iterable[Eigenvariable]:
        return sorted(set(self._iter_dischargeable_eigenvariables()), key=str)

    @override
    def build_renderer(self, *, conclusion: FormulaWithSubstitution | None = None) -> RuleApplicationRenderer:
        if conclusion is None:
            conclusion = self.conclusion

        if str(conclusion) == str(self.conclusion):
            line = str(conclusion)
        else:
            line = f'{self.conclusion} = {conclusion}'

        return RuleApplicationRenderer(
            line,
            [str(marker) for marker in self.get_marker_context()],
            self.rule.name,
            [premise.build_renderer() for premise in self.premises]
        )

    def get_marked_free_variables(self) -> Iterable[MarkedVariable]:
        discharged_markers = self.get_marker_context()
        discharged_eigen = {evar.var for evar in self.get_eigenvariable_context()}

        for application_premise in self.premises:
            for mvar in application_premise.tree.get_marked_free_variables():
                if mvar.marker not in discharged_markers and mvar.var not in discharged_eigen:
                    yield mvar

    def get_free_variables(self) -> Collection[Variable]:
        return {mvar.var for mvar in self.get_marked_free_variables()}

    def __str__(self) -> str:
        return self.build_renderer().render()


def apply(  # noqa: C901
    rule: NaturalDeductionRule,
    *args: ProofTree | RuleApplicationPremise,
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
        if eigen := get_main_eigenvariable(rule_premise, application_premise):
            if eigen.is_renamed() and eigen.var in get_formula_free_variables(eigen.formula):
                raise RuleApplicationError(f'The renamed eigenvariable {eigen.get_sub()} of the premise conclusion {eigen.formula} cannot be free in it')

            if eigen.var in application_premise.tree.get_free_variables():
                raise RuleApplicationError(f'The eigenvariable {eigen} cannot be free in the derivation of {application_premise.tree.conclusion}')

        if rule_premise.discharge:
            if application_premise.discharge is None:
                raise RuleApplicationError(f'The rule {rule.name} requires a discharge formula for premise number {i}')

            # Check if there is an eigenvariable in the discharge formula
            if eigen := get_discharge_eigenvariable(rule_premise, application_premise):
                if eigen.is_renamed() and eigen.var in get_formula_free_variables(eigen.formula):
                    raise RuleApplicationError(f'The renamed eigenvariable {eigen.get_sub()} of the dischargeable formula {eigen.formula} cannot be free in it')

                if any(mvar.var == eigen.var and mvar.marker != application_premise.marker for mvar in application_premise.tree.get_marked_free_variables()):
                    if application_premise.marker:
                        raise RuleApplicationError(f'The eigenvariable {eigen} cannot be free in the derivation of {application_premise.tree.conclusion}, except possibly in [{application_premise.discharge}]{to_superscript(str(application_premise.marker))}')

                    raise RuleApplicationError(f'The eigenvariable {eigen} cannot be free in the derivation of {application_premise.tree.conclusion}')

                if eigen.var in get_formula_free_variables(evaluate_substitution_spec(application_premise.tree.conclusion)):
                    raise RuleApplicationError(f'The discharge formula eigenvariable {eigen} cannot be free in the conclusion {application_premise.tree.conclusion} of premise number {i}')

            # Update instantiation
            instantiation |= infer_instantiation_from_formula_substitution_spec(
                rule_premise.discharge,
                application_premise.discharge
            )

        instantiation |= infer_instantiation_from_formula_substitution_spec(
            rule_premise.main,
            application_premise.main,
        )

    if rule.conclusion.sub:
        if not conclusion_sub:
            raise RuleApplicationError('Expected a substitution of the conclusion')

        instantiation |= infer_instantiation_from_term_substitution_spec(rule.conclusion.sub, conclusion_sub)

    return RuleApplicationTree(
        rule,
        instantiation,
        application_premises,
        instantiate_substitution_spec(rule.conclusion, instantiation)
    )


ProofTree = AssumptionTree | RuleApplicationTree
