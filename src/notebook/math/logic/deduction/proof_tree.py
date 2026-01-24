from collections.abc import Collection, Iterable, Mapping, Sequence
from dataclasses import dataclass
from typing import override

from ....support.inference import (
    AssumptionRenderer,
    InferenceTree,
    RuleApplicationRenderer,
)
from ....support.schemas import SchemaInstantiationError
from ..formulas import (
    Formula,
    FormulaPlaceholder,
    FormulaSchemaWithEigenvariable,
    FormulaWithSubstitution,
)
from ..instantiation import (
    AtomicLogicSchemaInstantiation,
    infer_instantiation_from_formula,
    infer_instantiation_from_formula_substitution_spec,
    instantiate_substitution,
    instantiate_term_schema,
)
from ..substitution import evaluate_substitution
from ..terms import Variable
from ..variables import get_formula_free_variables
from .exceptions import RuleApplicationError
from .markers import MarkedFormula, MarkedFormulaWithSubstitution, Marker
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

    def get_local_implicit_premises(self) -> Collection[Formula]:
        return set()

    def get_local_eigenvariables(self) -> Collection[Variable]:
        return set()

    def get_free_variables(
        self,
        eigen: Collection[Variable] = set(),
        discharged: Collection[Marker] = set()
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
    attachments: Sequence[None | MarkedFormula]


# This class is only needed to aid the construction of proof trees; we do not need attached substitutions in the final tree
@dataclass(frozen=True)
class RuleApplicationPremiseConfig:
    tree: ProofTree
    main: FormulaWithSubstitution
    attachments: Sequence[None | MarkedFormulaWithSubstitution]

    def eval(self) -> RuleApplicationPremise:
        return RuleApplicationPremise(
            self.tree,
            [att.eval() if att else None for att in self.attachments],
        )


def premise_config(
    *,
    tree: ProofTree,
    main: FormulaWithSubstitution | None = None,
    attachments: Sequence[None | MarkedFormula | MarkedFormulaWithSubstitution] = [],
) -> RuleApplicationPremiseConfig:
    return RuleApplicationPremiseConfig(
        tree,
        FormulaWithSubstitution.wrap(main or tree.conclusion),
        [MarkedFormulaWithSubstitution.wrap(att) if att else None for att in attachments],
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

    def _iter_implicit_premises(self) -> Iterable[Formula]:
        for schema in self.rule.conclusion.attachments:
            formula = evaluate_substitution(instantiate_substitution(schema, self.instantiation))

            for assumption in self._filter_assumptions(discharged_at_current_step=True):
                if assumption.formula == formula:
                    break
            else:
                yield formula

    def get_local_implicit_premises(self) -> Collection[Formula]:
        return set(self._iter_implicit_premises())

    @override
    def get_cumulative_assumptions(self) -> Collection[MarkedFormula]:
        return set(self._filter_assumptions(discharged_at_current_step=False))

    def get_locally_discharged_markers(self) -> Collection[Marker]:
        return {
            assumption.marker for assumption in self._filter_assumptions(discharged_at_current_step=True)
        }

    def _iter_current_eigenvariables(self) -> Iterable[Variable]:
        for rule_premise in self.rule.premises:
            if isinstance(rule_premise.main, FormulaSchemaWithEigenvariable):
                yield instantiate_term_schema(rule_premise.main.sub.dest, self.instantiation)

            for attachment_schema in rule_premise.attachments:
                if isinstance(attachment_schema, FormulaSchemaWithEigenvariable):
                    yield instantiate_term_schema(attachment_schema.sub.dest, self.instantiation)

    def get_local_eigenvariables(self) -> Collection[Variable]:
        return set(self._iter_current_eigenvariables())

    @override
    def build_renderer(self) -> RuleApplicationRenderer:
        return RuleApplicationRenderer(
            str(self.conclusion),
            [str(marker) for marker in self.get_locally_discharged_markers()],
            self.rule.name,
            [premise.tree.build_renderer() for premise in self.premises]
        )

    def _iter_free_variables(
        self,
        eigen: Collection[Variable],
        discharged: Collection[Marker]
    ) -> Iterable[Variable]:
        eigen_ = {*eigen, *self.get_local_eigenvariables()}
        discharged_ = {*discharged, *self.get_locally_discharged_markers()}

        for premise_tree in self.premises:
             yield from premise_tree.tree.get_free_variables(eigen_, discharged_)

        for premise in self.get_local_implicit_premises():
             for var in get_formula_free_variables(premise):
                if var not in eigen:
                    yield var

    def get_free_variables(
        self,
        eigen: Collection[Variable] = set(),
        discharged: Collection[Marker] = set()
    ) -> Collection[Variable]:
        return set(self._iter_free_variables(eigen, discharged))

    def __str__(self) -> str:
        return self.build_renderer().render()


def apply(  # noqa: C901,PLR0915
    rule: NaturalDeductionRule,
    *args: ProofTree | RuleApplicationPremiseConfig,
    instantiation: AtomicLogicSchemaInstantiation | None = None,
    implicit: Mapping[FormulaPlaceholder, Formula] | None = None,
    conclusion_config: FormulaWithSubstitution | None = None,
) -> RuleApplicationTree:
    if len(args) != len(rule.premises):
        raise RuleApplicationError(f'The rule {rule.name} has {len(rule.premises)} premises, but the application has {len(args)}')

    if instantiation is None:
        instantiation = AtomicLogicSchemaInstantiation(formula_mapping=implicit)
    elif implicit:
        raise RuleApplicationError('Cannot provide both an instantiation and implicit assumptions')

    marker_map = dict[Marker, Formula]()

    application_premises = [
        premise_config(tree=premise_arg, attachments=[None] * len(rule_premise.attachments))
        if isinstance(premise_arg, ProofTree)
        else premise_arg
        for rule_premise, premise_arg in zip(rule.premises, args, strict=True)
    ]

    for i, (rule_premise, application_premise) in enumerate(zip(rule.premises, application_premises, strict=True), start=1):
        for assumption in application_premise.tree.get_cumulative_assumptions():
            if assumption.marker is None:
                continue

            if assumption.marker in marker_map and marker_map[assumption.marker] != assumption.formula:
                raise RuleApplicationError('Multiple assumptions cannot have the same marker')

            marker_map[assumption.marker] = assumption.formula

        # Check if there is an eigenvariable in the main formula
        if isinstance(rule_premise.main, FormulaSchemaWithEigenvariable):
            if application_premise.main.sub is None or not isinstance(application_premise.main.sub.dest, Variable):
                raise RuleApplicationError(f'The schema {rule_premise.main} in rule {rule.name} requires a matching eigenvariable instance')

            eigen = application_premise.main.sub.dest

            if not application_premise.main.sub.is_noop() and eigen in get_formula_free_variables(application_premise.main.formula):
                raise RuleApplicationError(f'The eigenvariable {eigen} of the unsubstituted premise conclusion {application_premise.main.formula} cannot be free in it')

            if eigen in application_premise.tree.get_free_variables():
                raise RuleApplicationError(f'The eigenvariable {eigen} cannot be free in the derivation of {application_premise.tree.conclusion}')

        if len(application_premise.attachments) != len(rule_premise.attachments):
            if len(rule_premise.attachments) == 1:
                raise RuleApplicationError(f'The rule {rule.name} requires an attached formula for premise number {i}')

            raise RuleApplicationError(f'The rule {rule.name} requires {len(rule_premise.attachments)} attached formulas for premise number {i}')

        for attachment_schema, attachment in zip(rule_premise.attachments, application_premise.attachments, strict=True):
            if attachment is None:
                continue

            if isinstance(attachment_schema, FormulaSchemaWithEigenvariable):
                if attachment.payload.sub is None or not isinstance(attachment.payload.sub.dest, Variable):
                    raise RuleApplicationError(f'The schema {attachment_schema} in rule {rule.name} requires a matching eigenvariable instance')

                eigen = attachment.payload.sub.dest
                app_conclusion = application_premise.tree.conclusion

                if not attachment.payload.sub.is_noop() and eigen in get_formula_free_variables(attachment.payload.formula):
                    raise RuleApplicationError(f'The renamed eigenvariable {eigen} of the unsubstituted attached formula {attachment.payload.formula} cannot be free in it')

                if eigen in get_formula_free_variables(app_conclusion):
                    raise RuleApplicationError(f'The attached formula eigenvariable {eigen} cannot be free in the conclusion {app_conclusion} of premise number {i} of the rule {rule.name}')

                if eigen in application_premise.tree.get_free_variables(discharged={attachment.marker}):
                    raise RuleApplicationError(f'The eigenvariable {eigen} cannot be free in the derivation of {app_conclusion}, except possibly in {attachment.eval()}')

            # Update instantiation
            instantiation |= infer_instantiation_from_formula_substitution_spec(
                attachment_schema,
                attachment.payload
            )

        if application_premise.main:
            if rule_premise.main.sub is None:
                instantiation |= infer_instantiation_from_formula(
                    rule_premise.main.formula,
                    evaluate_substitution(application_premise.main),
                )
            else:
                instantiation |= infer_instantiation_from_formula_substitution_spec(
                    rule_premise.main,
                    application_premise.main,
                )

    if rule.conclusion.main.sub:
        if conclusion_config is None:
            raise RuleApplicationError(f'The rule {rule.name} requires a conclusion with an explicit substitution')

        instantiation |= infer_instantiation_from_formula_substitution_spec(rule.conclusion.main, conclusion_config)

    for attachment_schema in rule.conclusion.attachments:
        try:
            instantiate_substitution(attachment_schema, instantiation)
        except SchemaInstantiationError as err:
            raise RuleApplicationError(f'Cannot instantiate the implicit premise {attachment_schema} of the rule {rule.name}') from err

    if conclusion_config is None:
        conclusion_config = instantiate_substitution(rule.conclusion.main, instantiation)

    return RuleApplicationTree(
        rule,
        instantiation,
        [premise.eval() for premise in application_premises],
        evaluate_substitution(conclusion_config),
    )


ProofTree = AssumptionTree | RuleApplicationTree
