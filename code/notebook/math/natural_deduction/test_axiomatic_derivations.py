from collections.abc import Sequence
from textwrap import dedent

from ..fol.formulas import Formula
from ..fol.parsing.parser import parse_formula
from ..fol.signature import FOLSignature
from .axiomatic_derivations import AxiomaticDerivation, derivation_to_proof_tree, proof_tree_to_derivation
from .minimal_implicational_logic import IMPLICATIONAL_AXIOMS, get_identity_derivation


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

    assert t(get_identity_derivation(parse_formula(propositional_signature, 'p'))) == dedent('''\
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
        assert derivation == proof_tree_to_derivation(tree)

    t(['p'])
    t(['(p → q)', 'p', 'q'])
    t(get_identity_derivation(parse_formula(propositional_signature, 'p')))
