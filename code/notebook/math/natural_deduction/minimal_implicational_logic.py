from ..fol.alphabet import BinaryConnective
from ..fol.formulas import ConnectiveFormula, Formula, is_conditional
from .axiomatic_derivation import AxiomaticDerivation
from .parsing.parser import parse_schema


IMPLICATIONAL_AXIOMS = frozenset([
    parse_schema('(Φ → (Ψ → Φ))'),
    parse_schema('((Φ → (Ψ → Θ)) → ((Φ → Ψ) → (Φ → Θ)))'),
])


def get_identity_derivation_payload(formula: Formula) -> list[Formula]:
    """Axiomatic derivation of (P → P)"""
    goal = ConnectiveFormula(BinaryConnective.conditional, formula, formula)

    # The first two are axioms from the first schema
    a = ConnectiveFormula(BinaryConnective.conditional, formula, goal)
    b = ConnectiveFormula(BinaryConnective.conditional, formula, ConnectiveFormula(BinaryConnective.conditional, goal, formula))

    # This is an intermediate step obtained from axioms
    i = ConnectiveFormula(BinaryConnective.conditional, a, goal)

    # This is an axiom from the second schema
    c = ConnectiveFormula(BinaryConnective.conditional, b, i)

    return [a, b, c, i, goal]


def introduce_conclusion_hypothesis(derivation: AxiomaticDerivation, hypothesis: Formula) -> AxiomaticDerivation:
    if len(derivation.payload) == 0:
        return derivation

    *rest, conclusion = derivation.payload

    goal = ConnectiveFormula(BinaryConnective.conditional, hypothesis, conclusion)

    if derivation.is_axiom(goal) or derivation.is_premise(goal):
        return AxiomaticDerivation(
            axiom_schemas=derivation.axiom_schemas,
            payload=[goal]
        )

    if conclusion == hypothesis:
        return AxiomaticDerivation(
            axiom_schemas=derivation.axiom_schemas,
            payload=get_identity_derivation_payload(conclusion)
        )

    if derivation.is_axiom(conclusion) or derivation.is_premise(conclusion):
        return AxiomaticDerivation(
            axiom_schemas=derivation.axiom_schemas,
            payload=[
                ConnectiveFormula(
                    BinaryConnective.conditional,
                    conclusion,
                    ConnectiveFormula(BinaryConnective.conditional, hypothesis, conclusion)
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
    cond_deriv = introduce_conclusion_hypothesis(derivation.truncate(mp_config.conditional_index), hypothesis)
    antecetent_deriv = introduce_conclusion_hypothesis(derivation.truncate(mp_config.antecedent_index), hypothesis)

    dist = ConnectiveFormula(
        BinaryConnective.conditional,
        ConnectiveFormula(BinaryConnective.conditional, hypothesis, cond.a),
        ConnectiveFormula(BinaryConnective.conditional, hypothesis, cond.b)
    )

    return AxiomaticDerivation(
        axiom_schemas=derivation.axiom_schemas,
        payload=[
            *cond_deriv.payload,
            ConnectiveFormula(BinaryConnective.conditional, cond_deriv.get_conclusion(), dist),
            dist,
            *antecetent_deriv.payload,
            goal
        ]
    )
