from collections.abc import Sequence
from textwrap import dedent

from ...support.pytest import pytest_parametrize_kwargs, pytest_parametrize_lists
from ..fol.parsing import parse_propositional_formula
from .axiomatic_derivation import (
    AxiomaticDerivation,
    are_derivations_equivalent,
    derivation_to_proof_tree,
    proof_tree_to_derivation,
)
from .conftest import IDENTITY_DERIVATION
from .minimal_implicational_logic import IMPLICATIONAL_AXIOMS


@pytest_parametrize_kwargs(
    # Identical
    dict(
        a_payload=['p'],
        b_payload=['p']
    ),

    # One has an unnecessary axiom
    dict(
        a_payload=['(p → (q → p))', 'p'],
        b_payload=['p']
    ),

     # Distinct order of formulas
    dict(
        a_payload=['(p → q)', 'p', 'q'],
        b_payload=['p', '(p → q)', 'q']
    )
)
def test_are_derivations_equivalent_success(a_payload: Sequence[str], b_payload: Sequence[str]) -> None:
    a = AxiomaticDerivation(
        axiom_schemas=IMPLICATIONAL_AXIOMS,
        payload=[parse_propositional_formula(s) for s in a_payload]
    )

    b = AxiomaticDerivation(
        axiom_schemas=IMPLICATIONAL_AXIOMS,
        payload=[parse_propositional_formula(s) for s in b_payload]
    )

    assert are_derivations_equivalent(a, b)


@pytest_parametrize_kwargs(
    # One has an unnecessary premise
    dict(
        a_payload=['q', 'p'],
        b_payload=['p']
    ),

    # Distinct formulas with the same shape
    dict(
        a_payload=['(p → q)', 'p', 'q'],
        b_payload=['(q → p)', 'q', 'p']
    )
)
def test_are_derivations_equivalent_failure(a_payload: Sequence[str], b_payload: Sequence[str]) -> None:
    a = AxiomaticDerivation(
        axiom_schemas=IMPLICATIONAL_AXIOMS,
        payload=[parse_propositional_formula(s) for s in a_payload]
    )

    b = AxiomaticDerivation(
        axiom_schemas=IMPLICATIONAL_AXIOMS,
        payload=[parse_propositional_formula(s) for s in b_payload]
    )

    assert not are_derivations_equivalent(a, b)


@pytest_parametrize_kwargs(
    dict(
        payload=['p'],
        expected=dedent('''\
            [p]ᵃ
            '''
        )
    ),

    dict(
        payload=['(p → q)', 'p', 'q'],
        expected=dedent('''\
            [(p → q)]ᵃ    [p]ᵇ
            __________________ MP
                    q
            '''
        )
    ),

    dict(
        payload=IDENTITY_DERIVATION,
        expected=dedent('''\
            _________________________________________________ Ax    ___________________ Ax
            ((p → ((p → p) → p)) → ((p → (p → p)) → (p → p)))       (p → ((p → p) → p))
            ___________________________________________________________________________ MP    _____________ Ax
                                     ((p → (p → p)) → (p → p))                                (p → (p → p))
            _______________________________________________________________________________________________ MP
                                                        (p → p)
            '''
        )
    )
)
def test_derivation_to_proof_tree(payload: Sequence[str], expected: str) -> None:
    derivation = AxiomaticDerivation(
        axiom_schemas=IMPLICATIONAL_AXIOMS,
        payload=[parse_propositional_formula(s) for s in payload]
    )

    assert str(derivation_to_proof_tree(derivation)) == expected



@pytest_parametrize_lists(
    payload=[
        ['p'],
        ['(p → q)', 'p', 'q'],
        IDENTITY_DERIVATION
    ]
)
def test_proof_tree_to_derivation(payload: Sequence[str]) -> None:
    derivation = AxiomaticDerivation(
        axiom_schemas=IMPLICATIONAL_AXIOMS,
        payload=[parse_propositional_formula(s) for s in payload]
    )

    tree = derivation_to_proof_tree(derivation)
    assert are_derivations_equivalent(derivation, proof_tree_to_derivation(tree))
