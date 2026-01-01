from collections.abc import Sequence
from typing import overload

from ..alphabet import BinaryConnective
from ..formulas import ConnectiveFormula, Formula
from ..parsing import parse_formula_schema
from ..propositional import PropConnectiveFormula, PropFormula
from .axiomatic_derivation import AxiomaticDerivation, get_config_conditional_safe, get_premises
from .system import AxiomaticDerivationSystem


IMPLICATIONAL_AXIOMS = AxiomaticDerivationSystem({
    '→₊': parse_formula_schema('(φ → (ψ → φ))'),
    '↠': parse_formula_schema('((φ → (ψ → θ)) → ((φ → ψ) → (φ → θ)))'),
})


@overload
def make_conditional_formula(left: PropFormula, right: PropFormula) -> PropConnectiveFormula: ...
@overload
def make_conditional_formula(left: Formula, right: Formula) -> ConnectiveFormula: ...
def make_conditional_formula(left: Formula, right: Formula) -> ConnectiveFormula:
    if isinstance(left, PropFormula) and isinstance(right, PropFormula):
        return PropConnectiveFormula(BinaryConnective.CONDITIONAL, left, right)

    return ConnectiveFormula(BinaryConnective.CONDITIONAL, left, right)


def get_identity_derivation_payload(formula: Formula) -> Sequence[Formula]:
    """Axiomatic derivation of (p → p)"""
    goal = make_conditional_formula(formula, formula)

    # The first two are axioms from the first schema
    a = make_conditional_formula(formula, goal)
    b = make_conditional_formula(formula, make_conditional_formula(goal, formula))

    # This is an intermediate step obtained from axioms
    i = make_conditional_formula(a, goal)

    # This is an axiom from the second schema
    c = make_conditional_formula(b, i)

    return [a, b, c, i, goal]


def introduce_conclusion_hypothesis(system: AxiomaticDerivationSystem, derivation: AxiomaticDerivation, hypothesis: Formula) -> AxiomaticDerivation:
    if len(derivation.payload) == 0:
        return derivation

    *_rest, conclusion = derivation.payload

    goal = make_conditional_formula(hypothesis, conclusion)

    if system.is_axiom(goal) or goal in get_premises(system, derivation):
        return AxiomaticDerivation(payload=[goal])

    if conclusion == hypothesis:
        return AxiomaticDerivation(payload=get_identity_derivation_payload(conclusion))

    if system.is_axiom(conclusion) or conclusion in get_premises(system, derivation):
        return AxiomaticDerivation(
            payload=[
                make_conditional_formula(
                    conclusion,
                    make_conditional_formula(hypothesis, conclusion)
                ),
                conclusion,
                goal
            ]
        )

    mp_config = derivation.get_mp_config()

    if mp_config is None:
        return derivation

    cond = get_config_conditional_safe(derivation, mp_config)
    cond_deriv = introduce_conclusion_hypothesis(system, derivation.truncate(mp_config.conditional_index), hypothesis)
    antecetent_deriv = introduce_conclusion_hypothesis(system, derivation.truncate(mp_config.antecedent_index), hypothesis)

    dist = make_conditional_formula(
        make_conditional_formula(hypothesis, cond.left),
        make_conditional_formula(hypothesis, cond.right)
    )

    return AxiomaticDerivation(
        payload=[
            *cond_deriv.payload,
            make_conditional_formula(cond_deriv.get_conclusion(), dist),
            dist,
            *antecetent_deriv.payload,
            goal
        ]
    )
