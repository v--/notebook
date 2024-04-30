from collections.abc import Sequence
from textwrap import dedent

from ..fol.formulas import Formula
from ..fol.parsing.parser import parse_formula
from ..fol.signature import FOLSignature
from .axiomatic_derivation import (
    AxiomaticDerivation,
    are_derivations_equivalent,
    derivation_to_proof_tree,
    proof_tree_to_derivation,
)
from .minimal_implicational_logic import IMPLICATIONAL_AXIOMS, get_identity_derivation_payload


def test_are_derivations_equivalent(propositional_signature: FOLSignature) -> None:
    def t(a_payload: Sequence[str | Formula], b_payload: Sequence[str | Formula]) -> bool:
        a = AxiomaticDerivation(
            axiom_schemas=IMPLICATIONAL_AXIOMS,
            payload=[parse_formula(propositional_signature, s) if isinstance(s, str) else s for s in a_payload]
        )

        b = AxiomaticDerivation(
            axiom_schemas=IMPLICATIONAL_AXIOMS,
            payload=[parse_formula(propositional_signature, s) if isinstance(s, str) else s for s in b_payload]
        )

        return are_derivations_equivalent(a, b)

    assert t(['p'], ['p'])  # Identical
    assert t(['(p → (q → p))', 'p'], ['p'])  # One has an unnecessary axiom
    assert not t(['q', 'p'], ['p'])  # One has an unnecessary premise
    assert t(['(p → q)', 'p', 'q'], ['p', '(p → q)', 'q'])  # Distinct order of formulas
    assert not t(['(p → q)', 'p', 'q'], ['(q → p)', 'q', 'p'])  # Distinct formulas with the same shape


def test_derivation_to_proof_tree(propositional_signature: FOLSignature) -> None:
    def t(payload: Sequence[str | Formula]) -> str:
        derivation = AxiomaticDerivation(
            axiom_schemas=IMPLICATIONAL_AXIOMS,
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

    assert t(get_identity_derivation_payload(parse_formula(propositional_signature, 'p'))) == dedent('''\
        (MP) (p → p)
        ├── (MP) ((p → (p → p)) → (p → p))
        │   ├── (Ax) ((p → ((p → p) → p)) → ((p → (p → p)) → (p → p)))
        │   └── (Ax) (p → ((p → p) → p))
        └── (Ax) (p → (p → p))
        '''
    )


def test_proof_tree_to_derivation(propositional_signature: FOLSignature) -> None:
    def t(payload: Sequence[str | Formula]) -> None:
        derivation = AxiomaticDerivation(
            axiom_schemas=IMPLICATIONAL_AXIOMS,
            payload=[parse_formula(propositional_signature, s) if isinstance(s, str) else s for s in payload]
        )

        tree = derivation_to_proof_tree(derivation)
        assert are_derivations_equivalent(derivation, proof_tree_to_derivation(tree))

    t(['p'])
    t(['(p → q)', 'p', 'q'])
    t(get_identity_derivation_payload(parse_formula(propositional_signature, 'p')))
