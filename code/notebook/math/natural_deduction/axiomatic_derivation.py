from collections.abc import Iterable
from dataclasses import dataclass
from typing import NamedTuple

from ...exceptions import NotebookCodeError
from ...support.names import new_var_name
from ..fol.formulas import Formula, is_conditional
from .parsing import parse_rule
from .proof_tree import AssumptionTree, NaturalDeductionSystem, ProofTree, RuleApplicationTree
from .rules import Rule
from .schemas import FormulaPlaceholder, FormulaSchema
from .substitution import UniformSubstitution, build_substitution, is_schema_instance


class AxiomaticDerivationError(NotebookCodeError):
    pass


class InvalidDerivationError(AxiomaticDerivationError):
    pass


MODUS_PONENS = parse_rule('(MP) (φ → ψ), φ ⫢ ψ')


class ModusPonensConfig(NamedTuple):
    conditional_index: int
    antecedent_index: int
    conclusion_index: int


@dataclass
class AxiomaticDerivation:
    axiom_schemas: frozenset[FormulaSchema]
    payload: list[Formula]

    def __post_init__(self) -> None:
        assert len(self.payload) > 0

    def get_conclusion(self) -> Formula:
        return self.payload[-1]

    def is_axiom(self, formula: Formula) -> bool:
        return any(is_schema_instance(schema, formula) for schema in self.axiom_schemas)

    def get_mp_config(self, k: int | None = None) -> ModusPonensConfig | None:
        if k is None:
            k = len(self.payload) - 1

        formula = self.payload[k]

        for i, cond in enumerate(self.payload[:k]):
            if is_conditional(cond) and cond.b == formula:
                for j, antecedent in enumerate(self.payload):
                     if antecedent == cond.a:
                        return ModusPonensConfig(i, j, k)

        return None

    def iter_premises(self) -> Iterable[Formula]:
        for k, conclusion in enumerate(self.payload):
            if not self.is_axiom(conclusion) and self.get_mp_config(k) is None:
                yield conclusion

    def is_premise(self, formula: Formula) -> bool:
        return any(formula == premise for premise in self.iter_premises())

    def truncate(self, index: int) -> 'AxiomaticDerivation':
        assert index < len(self.payload)
        return AxiomaticDerivation(
            axiom_schemas=self.axiom_schemas,
            payload=self.payload[:index + 1]
        )


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


def are_derivations_equivalent(a: AxiomaticDerivation, b: AxiomaticDerivation) -> bool:
    if a.axiom_schemas != b.axiom_schemas:
        return False

    if a.get_conclusion() != b.get_conclusion():
        return False

    if set(a.iter_premises()) != set(b.iter_premises()):
        return False

    return _are_derivations_equivalent_recurse(a, b)


# This is alg:proof_tree_to_axiomatic_derivation in the monograph
def derivation_to_proof_tree(derivation: AxiomaticDerivation, used_markers: frozenset = frozenset()) -> ProofTree:
    conclusion = derivation.get_conclusion()
    system = NaturalDeductionSystem(
        frozenset(
            [MODUS_PONENS] + [
                Rule(name='Ax', premises=[], conclusion=axiom_schema)
                for axiom_schema in derivation.axiom_schemas
            ]
        )
    )

    if derivation.is_premise(conclusion):
        return AssumptionTree(system, conclusion, marker=new_var_name('u₁', used_markers))

    for rule in system.rules:
        if rule.name != 'Ax' or (substitution := build_substitution(rule.conclusion, conclusion)) is None:
            continue

        return RuleApplicationTree(
            system=system,
            rule=rule,
            substitution=substitution,
            subtrees=[]
        )

    mp_config = derivation.get_mp_config()

    if mp_config is None:
        raise AxiomaticDerivationError(f'Invalid derivation of {conclusion}')

    cond = derivation.payload[mp_config.conditional_index]
    assert is_conditional(cond)
    conditional_subtree = derivation_to_proof_tree(derivation.truncate(mp_config.conditional_index), used_markers)
    markers = frozenset(ass.marker for ass in conditional_subtree.iter_open_assumptions())
    antecedent_subtree = derivation_to_proof_tree(derivation.truncate(mp_config.antecedent_index), used_markers | markers)
    substitution = UniformSubstitution({
        FormulaPlaceholder('φ'): antecedent_subtree.conclusion,
        FormulaPlaceholder('ψ'): conclusion
    })

    return RuleApplicationTree(
        system=system,
        rule=MODUS_PONENS,
        substitution=substitution,
        subtrees=[conditional_subtree, antecedent_subtree]
    )


def _proof_tree_to_derivation_payload(tree: ProofTree) -> Iterable[Formula]:
    if isinstance(tree, RuleApplicationTree):
        for subtree in tree.subtrees:
            yield from _proof_tree_to_derivation_payload(subtree)

    yield tree.conclusion


# This is alg:axiomatic_derivation_to_proof_tree in the monograph
def proof_tree_to_derivation(tree: ProofTree) -> AxiomaticDerivation:
    return AxiomaticDerivation(
        axiom_schemas=frozenset(rule.conclusion for rule in tree.system.rules if rule is not MODUS_PONENS),
        payload=list(_proof_tree_to_derivation_payload(tree))
    )
