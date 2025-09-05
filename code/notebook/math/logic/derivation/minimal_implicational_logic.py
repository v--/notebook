from collections.abc import Sequence

from ..alphabet import BinaryConnective
from ..formulas import ConnectiveFormula, Formula, is_conditional
from ..parsing import parse_formula_schema
from .axiomatic_derivation import AxiomaticDerivation, get_premises
from .system import AxiomaticDerivationSystem


IMPLICATIONAL_AXIOMS = AxiomaticDerivationSystem({
    '→₊': parse_formula_schema('(φ → (ψ → φ))'),
    '↠': parse_formula_schema('((φ → (ψ → θ)) → ((φ → ψ) → (φ → θ)))'),
})


def get_identity_derivation_payload(formula: Formula) -> Sequence[Formula]:
    """Axiomatic derivation of (p → p)"""
    goal = ConnectiveFormula(BinaryConnective.CONDITIONAL, formula, formula)

    # The first two are axioms from the first schema
    a = ConnectiveFormula(BinaryConnective.CONDITIONAL, formula, goal)
    b = ConnectiveFormula(BinaryConnective.CONDITIONAL, formula, ConnectiveFormula(BinaryConnective.CONDITIONAL, goal, formula))

    # This is an intermediate step obtained from axioms
    i = ConnectiveFormula(BinaryConnective.CONDITIONAL, a, goal)

    # This is an axiom from the second schema
    c = ConnectiveFormula(BinaryConnective.CONDITIONAL, b, i)

    return [a, b, c, i, goal]


def introduce_conclusion_hypothesis(system: AxiomaticDerivationSystem, derivation: AxiomaticDerivation, hypothesis: Formula) -> AxiomaticDerivation:
    if len(derivation.payload) == 0:
        return derivation

    *rest, conclusion = derivation.payload

    goal = ConnectiveFormula(BinaryConnective.CONDITIONAL, hypothesis, conclusion)

    if system.is_axiom(goal) or goal in get_premises(system, derivation):
        return AxiomaticDerivation(payload=[goal])

    if conclusion == hypothesis:
        return AxiomaticDerivation(payload=get_identity_derivation_payload(conclusion))

    if system.is_axiom(conclusion) or conclusion in get_premises(system, derivation):
        return AxiomaticDerivation(
            payload=[
                ConnectiveFormula(
                    BinaryConnective.CONDITIONAL,
                    conclusion,
                    ConnectiveFormula(BinaryConnective.CONDITIONAL, hypothesis, conclusion)
                ),
                conclusion,
                goal
            ]
        )

    mp_config = derivation.get_mp_config()

    if mp_config is None:
        return derivation

    cond = derivation.payload[mp_config.conditional_index]
    assert is_conditional(cond)
    cond_deriv = introduce_conclusion_hypothesis(system, derivation.truncate(mp_config.conditional_index), hypothesis)
    antecetent_deriv = introduce_conclusion_hypothesis(system, derivation.truncate(mp_config.antecedent_index), hypothesis)

    dist = ConnectiveFormula(
        BinaryConnective.CONDITIONAL,
        ConnectiveFormula(BinaryConnective.CONDITIONAL, hypothesis, cond.left),
        ConnectiveFormula(BinaryConnective.CONDITIONAL, hypothesis, cond.right)
    )

    return AxiomaticDerivation(
        payload=[
            *cond_deriv.payload,
            ConnectiveFormula(BinaryConnective.CONDITIONAL, cond_deriv.get_conclusion(), dist),
            dist,
            *antecetent_deriv.payload,
            goal
        ]
    )
