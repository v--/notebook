from collections.abc import Sequence
from textwrap import dedent

from ..fol.formulas import Formula
from ..fol.parsing.parser import parse_formula
from ..fol.signature import FOLSignature
from .derivation import (
    AxiomaticDerivation,
    derivation_to_proof_tree,
    get_identity_derivation,
    introduce_conclusion_hypothesis,
    proof_tree_to_derivation,
)
from .rules import FormulaPlaceholder


def test_minimal_implicational_derivation_premises(propositional_signature: FOLSignature, implicational_axioms: frozenset[FormulaPlaceholder]) -> None:
    def t(payload: Sequence[str | Formula]) -> list[str]:
        derivation = AxiomaticDerivation(
            axiom_schemas=implicational_axioms,
            payload=[parse_formula(propositional_signature, s) if isinstance(s, str) else s for s in payload]
        )

        return [str(f) for f in derivation.iter_premises()]

    assert t(['(p → (q → p))']) == []
    assert t(['(p → (p → p))']) == []

    assert t(['p']) == ['p']

    assert t(get_identity_derivation(parse_formula(propositional_signature, 'p'))) == []


def test_introduce_conclusion_hypothesis(propositional_signature: FOLSignature, implicational_axioms: frozenset[FormulaPlaceholder]) -> None:
    def t(seq: list[str], /, hypothesis: str) -> list[str]:
        derivation = AxiomaticDerivation(
            axiom_schemas=implicational_axioms,
            payload=[parse_formula(propositional_signature, s) for s in seq]
        )

        hypothesis_formula = parse_formula(propositional_signature, hypothesis)
        relativized = introduce_conclusion_hypothesis(derivation, hypothesis_formula)
        return [str(formula) for formula in relativized.payload]

    assert t(['p'], hypothesis='p') == [
        str(formula) for formula in get_identity_derivation(parse_formula(propositional_signature, 'p'))
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


def test_derivation_to_proof_tree(propositional_signature: FOLSignature, implicational_axioms: frozenset[FormulaPlaceholder]) -> None:
    def t(payload: Sequence[str | Formula]) -> str:
        derivation = AxiomaticDerivation(
            axiom_schemas=implicational_axioms,
            payload=[parse_formula(propositional_signature, s) if isinstance(s, str) else s for s in payload]
        )

        return str(derivation_to_proof_tree(derivation))

    assert t(['p']) == dedent('''\
        [p]ᵘ₁
        '''
    )

    assert t(['(p → q)', 'p', 'q']) == dedent('''\
        (MP) q
        ├── [(p → q)]ᵘ₁
        └── [p]ᵘ₂
        '''
    )

    assert t(get_identity_derivation(parse_formula(propositional_signature, 'p'))) == dedent('''\
        (MP) (p → p)
        ├── (MP) ((p → (p → p)) → (p → p))
        │   ├── (Ax) ((p → ((p → p) → p)) → ((p → (p → p)) → (p → p)))
        │   └── (Ax) (p → ((p → p) → p))
        └── (Ax) (p → (p → p))
        '''
    )


def test_proof_tree_to_derivation(propositional_signature: FOLSignature, implicational_axioms: frozenset[FormulaPlaceholder]) -> None:
    def t(payload: Sequence[str | Formula]) -> None:
        derivation = AxiomaticDerivation(
            axiom_schemas=implicational_axioms,
            payload=[parse_formula(propositional_signature, s) if isinstance(s, str) else s for s in payload]
        )

        tree = derivation_to_proof_tree(derivation)
        assert derivation == proof_tree_to_derivation(tree)

    t(['p'])
    t(['(p → q)', 'p', 'q'])
    t(get_identity_derivation(parse_formula(propositional_signature, 'p')))
