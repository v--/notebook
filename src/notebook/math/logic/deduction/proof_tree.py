from dataclasses import dataclass
from typing import TYPE_CHECKING, override

from notebook.math.logic.formulas import ExtendedFormulaPlaceholder, Formula, FormulaWithSubstitution
from notebook.math.logic.instantiation import (
    AtomicLogicSchemaInstantiation,
    infer_instantiation_from_formula,
    instantiate_formula_schema,
    instantiate_term_schema,
)
from notebook.math.logic.substitution import evaluate_substitution
from notebook.math.logic.terms import EigenSchemaSubstitutionSpec, Variable
from notebook.math.logic.variables import get_formula_free_variables
from notebook.support.coderefs import collector
from notebook.support.inference import AssumptionRenderer, InferenceTree, RuleApplicationRenderer

from .exceptions import RuleApplicationError
from .markers import MarkedFormula, MarkedFormulaWithSubstitution, Marker


if TYPE_CHECKING:
    from collections.abc import Collection, Iterable, Sequence

    from .system import NaturalDeductionRule


@dataclass(frozen=True)
class AssumptionTree(InferenceTree[Formula, MarkedFormula]):
    conclusion: Formula
    marker: Marker

    @override
    def get_cumulative_assumptions(self) -> Collection[MarkedFormula]:
        return {MarkedFormula(self.conclusion, self.marker)}

    def get_locally_discharged_markers(self) -> Collection[Marker]:
        return [self.marker]

    @override
    def build_renderer(self) -> AssumptionRenderer:
        return AssumptionRenderer(
            str(self.conclusion),
            marker=str(self.marker),
        )

    def get_local_eigenvariables(self) -> Collection[Variable]:  # noqa: PLR6301
        return set()

    def get_open_variables(
        self,
        eigen: Collection[Variable] = set(),
        discharged: Collection[Marker] = set(),
    ) -> Collection[Variable]:
        if self.marker in discharged:
            return set()

        return {
            var for var in get_formula_free_variables(self.conclusion)
            if var not in eigen
        }

    def __str__(self) -> str:
        return self.build_renderer().render()


def assume(assumption: Formula, marker: Marker) -> AssumptionTree:
    return AssumptionTree(assumption, marker)


@dataclass(frozen=True)
class RuleApplicationPremise:
    tree: ProofTree
    attachments: Sequence[MarkedFormula | None]


# This class is only needed to aid the construction of proof trees; we do not need attached substitutions in the final tree
@dataclass(frozen=True)
class RuleApplicationPremiseConfig:
    tree: ProofTree
    main: Formula | FormulaWithSubstitution
    attachments: Sequence[MarkedFormula | MarkedFormulaWithSubstitution | None]

    def eval(self) -> RuleApplicationPremise:
        return RuleApplicationPremise(
            self.tree,
            [att.eval() if isinstance(att, MarkedFormulaWithSubstitution) else att for att in self.attachments],
        )


def premise_config(
    *,
    tree: ProofTree,
    main: FormulaWithSubstitution | None = None,
    attachments: Sequence[MarkedFormula | MarkedFormulaWithSubstitution | None] = [],
) -> RuleApplicationPremiseConfig:
    return RuleApplicationPremiseConfig(
        tree,
        main or tree.conclusion,
        attachments,
    )


@dataclass(frozen=True)
class RuleApplicationTree(InferenceTree[Formula, MarkedFormula]):
    rule: NaturalDeductionRule
    instantiation: AtomicLogicSchemaInstantiation
    premises: Sequence[RuleApplicationPremise]
    conclusion: Formula

    def _filter_assumptions(self, *, discharged_at_current_step: bool) -> Iterable[MarkedFormula]:
        for premise in self.premises:
            for assumption in premise.tree.get_cumulative_assumptions():
                is_discharged_at_current_step = any(att == assumption for att in premise.attachments)

                if discharged_at_current_step == is_discharged_at_current_step:
                    yield assumption

    @override
    def get_cumulative_assumptions(self) -> Collection[MarkedFormula]:
        return set(self._filter_assumptions(discharged_at_current_step=False))

    def get_locally_discharged_markers(self) -> Collection[Marker]:
        return {
            assumption.marker for assumption in self._filter_assumptions(discharged_at_current_step=True)
        }

    def _iter_current_eigenvariables(self) -> Iterable[Variable]:
        for rule_premise in self.rule.premises:
            if (
                isinstance(rule_premise.main, ExtendedFormulaPlaceholder) and
                isinstance(rule_premise.main.sub, EigenSchemaSubstitutionSpec)
            ):
                yield instantiate_term_schema(rule_premise.main.sub.dest, self.instantiation)

            for attachment_schema in rule_premise.attachments:
                if (
                    isinstance(attachment_schema, ExtendedFormulaPlaceholder) and
                    isinstance(attachment_schema.sub, EigenSchemaSubstitutionSpec)
                ):
                    yield instantiate_term_schema(attachment_schema.sub.dest, self.instantiation)

    def get_local_eigenvariables(self) -> Collection[Variable]:
        return set(self._iter_current_eigenvariables())

    @override
    def build_renderer(self) -> RuleApplicationRenderer:
        return RuleApplicationRenderer(
            str(self.conclusion),
            [str(marker) for marker in self.get_locally_discharged_markers()],
            self.rule.name,
            [premise.tree.build_renderer() for premise in self.premises],
        )

    def _iter_open_variables(
        self,
        eigen: Collection[Variable],
        discharged: Collection[Marker],
    ) -> Iterable[Variable]:
        eigen_ = {*eigen, *self.get_local_eigenvariables()}
        discharged_ = {*discharged, *self.get_locally_discharged_markers()}

        for premise_tree in self.premises:
            yield from premise_tree.tree.get_open_variables(eigen_, discharged_)

    def get_open_variables(
        self,
        eigen: Collection[Variable] = set(),
        discharged: Collection[Marker] = set(),
    ) -> Collection[Variable]:
        return set(self._iter_open_variables(eigen, discharged))

    def __str__(self) -> str:
        return self.build_renderer().render()


def _infer_application_instantiation(
    rule: NaturalDeductionRule,
    application_premises: Sequence[RuleApplicationPremiseConfig],
    instantiation: AtomicLogicSchemaInstantiation | None = None,
    conclusion_config: FormulaWithSubstitution | None = None,
) -> AtomicLogicSchemaInstantiation:
    result = instantiation or AtomicLogicSchemaInstantiation()

    # Infer instantiation
    for rule_premise, application_premise in zip(rule.premises, application_premises, strict=True):
        for attachment_schema, attachment in zip(rule_premise.attachments, application_premise.attachments, strict=True):
            if attachment:
                result |= infer_instantiation_from_formula(
                    attachment_schema,
                    attachment.payload if isinstance(attachment, MarkedFormulaWithSubstitution) else attachment.formula,
                )

        if application_premise.main:
            result |= infer_instantiation_from_formula(
                rule_premise.main,
                application_premise.main,
            )

    if isinstance(rule.conclusion, ExtendedFormulaPlaceholder) and rule.conclusion.sub:
        if conclusion_config is None:
            raise RuleApplicationError(f'The rule {rule.name} requires a conclusion with an explicit substitution')

        result |= infer_instantiation_from_formula(rule.conclusion, conclusion_config)

    return result


@collector.ref('def:fol_natural_deduction_proof_tree')
def apply(  # noqa: C901
    rule: NaturalDeductionRule,
    *args: ProofTree | RuleApplicationPremiseConfig,
    instantiation: AtomicLogicSchemaInstantiation | None = None,
    conclusion_config: FormulaWithSubstitution | None = None,
) -> RuleApplicationTree:
    if len(args) != len(rule.premises):
        raise RuleApplicationError(f'The rule {rule.name} has {len(rule.premises)} premises, but the application has {len(args)}')

    application_premises = [
        premise_config(tree=premise_arg, attachments=[None] * len(rule_premise.attachments))
        if isinstance(premise_arg, ProofTree)
        else premise_arg
        for rule_premise, premise_arg in zip(rule.premises, args, strict=True)
    ]

    instantiation = _infer_application_instantiation(
        rule, application_premises, instantiation, conclusion_config,
    )

    marker_map = dict[Marker, Formula]()

    if conclusion_config:
        conclusion = evaluate_substitution(conclusion_config)
    else:
        conclusion = instantiate_formula_schema(rule.conclusion, instantiation)

    for i, (rule_premise, application_premise) in enumerate(zip(rule.premises, application_premises, strict=True), start=1):
        for assumption in application_premise.tree.get_cumulative_assumptions():
            if assumption.marker is None:
                continue

            if assumption.marker in marker_map and marker_map[assumption.marker] != assumption.formula:
                raise RuleApplicationError('Multiple assumptions cannot have the same marker')

            marker_map[assumption.marker] = assumption.formula

        # Check if there is an eigenvariable in the main formula
        if (
            isinstance(rule_premise.main, ExtendedFormulaPlaceholder) and
            isinstance(rule_premise.main.sub, EigenSchemaSubstitutionSpec)
        ):
            if not isinstance(application_premise.main, FormulaWithSubstitution) or not isinstance(application_premise.main.sub.dest, Variable):
                raise RuleApplicationError(f'The schema {rule_premise.main} in rule {rule.name} requires a matching eigenvariable instance')

            eigen = application_premise.main.sub.dest

            if not application_premise.main.sub.is_noop() and eigen in get_formula_free_variables(application_premise.main.formula):
                raise RuleApplicationError(f'The eigenvariable {eigen} of the unsubstituted premise conclusion {application_premise.main.formula} cannot be free in it')

            if eigen in get_formula_free_variables(conclusion):
                raise RuleApplicationError(f'The attached formula eigenvariable {eigen} cannot be free in the conclusion {conclusion} of the rule {rule.name}')

            if eigen in application_premise.tree.get_open_variables():
                raise RuleApplicationError(f'The eigenvariable {eigen} cannot be free in the derivation of {application_premise.tree.conclusion}')

        if len(application_premise.attachments) != len(rule_premise.attachments):
            if len(rule_premise.attachments) == 1:
                raise RuleApplicationError(f'The rule {rule.name} requires an attached formula for premise number {i}')

            raise RuleApplicationError(f'The rule {rule.name} requires {len(rule_premise.attachments)} attached formulas for premise number {i}')

        for attachment_schema, attachment in zip(rule_premise.attachments, application_premise.attachments, strict=True):
            if (
                attachment is None or
                not isinstance(attachment_schema, ExtendedFormulaPlaceholder) or
                not isinstance(attachment_schema.sub, EigenSchemaSubstitutionSpec)
            ):
                continue

            if not isinstance(attachment, MarkedFormulaWithSubstitution) or not isinstance(attachment.payload.sub.dest, Variable):
                raise RuleApplicationError(f'The schema {attachment_schema} in rule {rule.name} requires a matching eigenvariable instance')

            eigen = attachment.payload.sub.dest
            app_conclusion = application_premise.tree.conclusion

            if not attachment.payload.sub.is_noop() and eigen in get_formula_free_variables(attachment.payload.formula):
                raise RuleApplicationError(f'The renamed eigenvariable {eigen} of the unsubstituted attached formula {attachment.payload.formula} cannot be free in it')

            if eigen in get_formula_free_variables(app_conclusion):
                raise RuleApplicationError(f'The attached formula eigenvariable {eigen} cannot be free in the conclusion {app_conclusion} of premise number {i} of the rule {rule.name}')

            if eigen in application_premise.tree.get_open_variables(discharged={attachment.marker}):
                raise RuleApplicationError(f'The eigenvariable {eigen} cannot be free in the derivation of {app_conclusion}, except possibly in {attachment.eval()}')

    return RuleApplicationTree(
        rule,
        instantiation,
        [premise.eval() for premise in application_premises],
        conclusion,
    )


ProofTree = AssumptionTree | RuleApplicationTree
