from collections.abc import Sequence

from ..fol.formulas import Formula
from ..fol.parsing import parse_propositional_formula
from .axiomatic_derivation import AxiomaticDerivation
from .minimal_implicational_logic import (
    IMPLICATIONAL_AXIOMS,
    get_identity_derivation_payload,
    introduce_conclusion_hypothesis,
)


def test_minimal_implicational_derivation_premises() -> None:
    def t(payload: Sequence[str | Formula]) -> Sequence[str]:
        derivation = AxiomaticDerivation(
            axiom_schemas=IMPLICATIONAL_AXIOMS,
            payload=[parse_propositional_formula(s) if isinstance(s, str) else s for s in payload]
        )

        return [str(f) for f in derivation.iter_premises()]

    assert t(['(p → (q → p))']) == []
    assert t(['(p → (p → p))']) == []

    assert t(['p']) == ['p']

    assert t(get_identity_derivation_payload(parse_propositional_formula('p'))) == []


def test_introduce_conclusion_hypothesis() -> None:
    def t(seq: Sequence[str], /, hypothesis: str) -> Sequence[str]:
        derivation = AxiomaticDerivation(
            axiom_schemas=IMPLICATIONAL_AXIOMS,
            payload=[parse_propositional_formula(s) for s in seq]
        )

        hypothesis_formula = parse_propositional_formula(hypothesis)
        relativized = introduce_conclusion_hypothesis(derivation, hypothesis_formula)
        return [str(formula) for formula in relativized.payload]

    assert t(['p'], hypothesis='p') == [
        str(formula) for formula in get_identity_derivation_payload(parse_propositional_formula('p'))
    ]

    assert t(['q'], hypothesis='p') == [
        '(q → (p → q))',
        'q',
        '(p → q)'
    ]

    assert t(['p', '(p → q)', 'q'], hypothesis='p') == ['(p → q)']
    assert t(['(p → q)', 'p', 'q'], hypothesis='p') == ['(p → q)']

    assert t(['(p → q)', '(q → r)', 'p', 'q', 'r'], hypothesis='p') == [
        '((q → r) → (p → (q → r)))',
        '(q → r)',
        '(p → (q → r))',
        '((p → (q → r)) → ((p → q) → (p → r)))',
        '((p → q) → (p → r))',
        '(p → q)',
        '(p → r)'
    ]

    assert t(['(p → (q → r))', 'p', '(q → r)', 'q', 'r'], hypothesis='p') == [
        '(p → (q → r))',
        '((p → (q → r)) → ((p → q) → (p → r)))',
        '((p → q) → (p → r))',
        '(q → (p → q))',
        'q',
        '(p → q)',
        '(p → r)'
    ]
