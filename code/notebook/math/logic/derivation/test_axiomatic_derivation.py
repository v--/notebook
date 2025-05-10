from collections.abc import Sequence
from textwrap import dedent

from ....support.pytest import pytest_parametrize_kwargs, pytest_parametrize_lists
from ..parsing import parse_propositional_formula
from .axiomatic_derivation import (
    AxiomaticDerivation,
    are_derivations_equivalent,
    derivation_to_proof_tree,
    proof_tree_to_derivation,
)
from .minimal_implicational_logic import IMPLICATIONAL_AXIOMS, get_identity_derivation_payload
from .system import derivation_system_to_natural_deduction_system


IDENTITY_DERIVATION = [
    str(f) for f in
    get_identity_derivation_payload(parse_propositional_formula('p'))
]


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
        payload=[parse_propositional_formula(s) for s in a_payload]
    )

    b = AxiomaticDerivation(
        payload=[parse_propositional_formula(s) for s in b_payload]
    )

    assert are_derivations_equivalent(IMPLICATIONAL_AXIOMS, a, b)


@pytest_parametrize_kwargs(
    # One has an unnecessary premise
    dict(
        a_payload=['q', 'p'],
        b_payload=['p']
    ),

    # Distinct instance of the same schema
    dict(
        a_payload=['(p → q)', 'p', 'q'],
        b_payload=['(q → p)', 'q', 'p']
    )
)
def test_are_derivations_equivalent_failure(a_payload: Sequence[str], b_payload: Sequence[str]) -> None:
    a = AxiomaticDerivation(
        payload=[parse_propositional_formula(s) for s in a_payload]
    )

    b = AxiomaticDerivation(
        payload=[parse_propositional_formula(s) for s in b_payload]
    )

    assert not are_derivations_equivalent(IMPLICATIONAL_AXIOMS, a, b)


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
            _________________________________________________ ↠    ___________________ →₊
            ((p → ((p → p) → p)) → ((p → (p → p)) → (p → p)))      (p → ((p → p) → p))
            __________________________________________________________________________ MP    _____________ →₊
                                    ((p → (p → p)) → (p → p))                                (p → (p → p))
            ______________________________________________________________________________________________ MP
                                                       (p → p)
            '''
        )
    )
)
def test_derivation_to_proof_tree(payload: Sequence[str], expected: str) -> None:
    derivation = AxiomaticDerivation(
        payload=[parse_propositional_formula(s) for s in payload]
    )

    assert str(derivation_to_proof_tree(IMPLICATIONAL_AXIOMS, derivation)) == expected



@pytest_parametrize_lists(
    payload=[
        ['p'],
        ['(p → q)', 'p', 'q'],
        IDENTITY_DERIVATION
    ]
)
def test_proof_tree_to_derivation(payload: Sequence[str]) -> None:
    derivation = AxiomaticDerivation(
        payload=[parse_propositional_formula(s) for s in payload]
    )

    tree = derivation_to_proof_tree(IMPLICATIONAL_AXIOMS, derivation)
    nd_system = derivation_system_to_natural_deduction_system(IMPLICATIONAL_AXIOMS)
    assert are_derivations_equivalent(IMPLICATIONAL_AXIOMS, derivation, proof_tree_to_derivation(nd_system, tree))
