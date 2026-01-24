from collections.abc import Collection, Iterable, Sequence
from dataclasses import dataclass
from typing import NamedTuple

from ....support.schemas import SchemaInferenceError
from ..alphabet import BinaryConnective
from ..deduction import (
    Marker,
    NaturalDeductionSystem,
    ProofTree,
    RuleApplicationPremise,
    RuleApplicationTree,
    assume,
    new_marker,
)
from ..formulas import ConnectiveFormula, Formula
from ..instantiation import AtomicLogicSchemaInstantiation, infer_instantiation_from_formula
from ..parsing import parse_formula_placeholder
from .exceptions import AxiomaticDerivationError
from .system import AxiomaticDerivationSystem, derivation_system_to_natural_deduction_system


class ModusPonensConfig(NamedTuple):
    conditional_index: int
    antecedent_index: int
    conclusion_index: int


@dataclass(frozen=True)
class AxiomaticDerivation:
    payload: Sequence[Formula]

    def __getitem__(self, index: int) -> Formula:
        return self.payload[index]

    def get_conclusion(self) -> Formula:
        return self.payload[-1]

    def get_mp_config(self, k: int | None = None) -> ModusPonensConfig | None:
        if k is None:
            k = len(self.payload) - 1

        formula = self.payload[k]

        for i, cond in enumerate(self.payload[:k]):
            if isinstance(cond, ConnectiveFormula) and cond.conn == BinaryConnective.CONDITIONAL and cond.right == formula:
                for j, antecedent in enumerate(self.payload):
                     if antecedent == cond.left:
                        return ModusPonensConfig(i, j, k)

        return None

    def truncate(self, index: int) -> AxiomaticDerivation:
        assert index < len(self.payload)
        return AxiomaticDerivation(payload=self.payload[:index + 1])


def get_config_conditional_safe(derivation: AxiomaticDerivation, mp_config: ModusPonensConfig) -> ConnectiveFormula:
    formula = derivation[mp_config.conditional_index]

    if not isinstance(formula, ConnectiveFormula) or formula.conn != BinaryConnective.CONDITIONAL:
        raise AxiomaticDerivationError(f'Invalid conditional {formula} in axiomatic derivation')

    return formula


def _are_derivations_equivalent_recurse(a: AxiomaticDerivation, b: AxiomaticDerivation) -> bool:
    if a.get_conclusion() != b.get_conclusion():
        return False

    a_config = a.get_mp_config()
    b_config = b.get_mp_config()

    if a_config is None and b_config is None:
        return True

    if a_config is None or b_config is None:
        return False

    return _are_derivations_equivalent_recurse(
        a.truncate(a_config.conditional_index),
        b.truncate(b_config.conditional_index)
    ) and _are_derivations_equivalent_recurse(
        a.truncate(a_config.antecedent_index),
        b.truncate(b_config.antecedent_index)
    )


def are_derivations_equivalent(ad_system: AxiomaticDerivationSystem, a: AxiomaticDerivation, b: AxiomaticDerivation) -> bool:
    if a.get_conclusion() != b.get_conclusion():
        return False

    if get_premises(ad_system, a) != get_premises(ad_system, b):
        return False

    return _are_derivations_equivalent_recurse(a, b)


def get_premises(ad_system: AxiomaticDerivationSystem, derivation: AxiomaticDerivation) -> Collection[Formula]:
    return {
        conclusion
        for k, conclusion in enumerate(derivation.payload)
        if derivation.get_mp_config(k) is None and not ad_system.is_axiom(conclusion)
    }


# This is alg:proof_tree_to_axiomatic_derivation in the monograph
def derivation_to_proof_tree(ad_system: AxiomaticDerivationSystem, derivation: AxiomaticDerivation, used_markers: Collection[Marker] = set()) -> ProofTree:
    conclusion = derivation.get_conclusion()

    if conclusion in get_premises(ad_system, derivation):
        return assume(conclusion, new_marker(used_markers))

    nd_system = derivation_system_to_natural_deduction_system(ad_system)

    for rule_name, axiom_schema in ad_system.axiom_schemas.items():
        try:
            instantiation = infer_instantiation_from_formula(axiom_schema, conclusion)
        except SchemaInferenceError:
            continue
        else:
            return RuleApplicationTree(
                nd_system[rule_name],
                instantiation,
                premises=[],
                conclusion=conclusion,
                implicit_variables=set()
            )

    mp_config = derivation.get_mp_config()

    if mp_config is None:
        raise AxiomaticDerivationError(f'Invalid derivation of {conclusion}')

    conditional_premise = RuleApplicationPremise(
        tree=derivation_to_proof_tree(ad_system, derivation.truncate(mp_config.conditional_index), used_markers),
        attachments=[]
    )

    markers = conditional_premise.tree.get_locally_discharged_markers()
    antecedent_premise = RuleApplicationPremise(
        tree=derivation_to_proof_tree(ad_system, derivation.truncate(mp_config.antecedent_index), {*used_markers, *markers}),
        attachments=[]
    )

    instantiation = AtomicLogicSchemaInstantiation(
        formula_mapping={
            parse_formula_placeholder('φ'): antecedent_premise.tree.conclusion,
            parse_formula_placeholder('ψ'): conclusion
        }
    )

    return RuleApplicationTree(
        nd_system['MP'],
        instantiation,
        premises=[conditional_premise, antecedent_premise],
        conclusion=conclusion,
        implicit_variables=set()
    )


def _proof_tree_to_derivation_payload(tree: ProofTree) -> Iterable[Formula]:
    if isinstance(tree, RuleApplicationTree):
        for premise in tree.premises:
            yield from _proof_tree_to_derivation_payload(premise.tree)

    yield tree.conclusion


# This is alg:axiomatic_proof_tree_to_derivation in the monograph
def proof_tree_to_derivation(ad_system: NaturalDeductionSystem, tree: ProofTree) -> AxiomaticDerivation:  # noqa: ARG001
    return AxiomaticDerivation(
        payload=list(_proof_tree_to_derivation_payload(tree))
    )
