from collections.abc import Collection, Sequence

from ...support.pytest import pytest_parametrize_kwargs
from ..fol.parsing import parse_propositional_formula
from .axiomatic_derivation import AxiomaticDerivation
from .conftest import IDENTITY_DERIVATION
from .minimal_implicational_logic import (
    IMPLICATIONAL_AXIOMS,
    introduce_conclusion_hypothesis,
)


@pytest_parametrize_kwargs(
    dict(
        payload=[],
        expected=set()
    ),

    dict(
        payload=['(p → (q → p))'],
        expected=set()
    ),

    dict(
        payload=['p'],
        expected={'p'}
    ),

    dict(
        payload=IDENTITY_DERIVATION,
        expected=set()
    ),
)
def test_minimal_implicational_derivation_premises(payload: Sequence[str], expected: Collection[str]) -> None:
    derivation = AxiomaticDerivation(
        axiom_schemas=IMPLICATIONAL_AXIOMS,
        payload=[parse_propositional_formula(s) for s in payload]
    )

    assert set(map(str, derivation.iter_premises())) == expected


@pytest_parametrize_kwargs(
    dict(
        payload=['p'],
        hypothesis='p',
        expected=IDENTITY_DERIVATION
    ),

    dict(
        payload=['q'],
        hypothesis='p',
        expected=[
            '(q → (p → q))',
            'q',
            '(p → q)'
        ]
    ),

    dict(
        payload=['p', '(p → q)', 'q'],
        hypothesis='p',
        expected=['(p → q)']
    ),

    dict(
        payload=['(p → q)', 'p', 'q'],
        hypothesis='p',
        expected=['(p → q)']
    ),

    dict(
        payload=['(p → q)', '(q → r)', 'p', 'q', 'r'],
        hypothesis='p',
        expected=[
            '((q → r) → (p → (q → r)))',
            '(q → r)',
            '(p → (q → r))',
            '((p → (q → r)) → ((p → q) → (p → r)))',
            '((p → q) → (p → r))',
            '(p → q)',
            '(p → r)'
        ]
    ),

    dict(
        payload=['(p → (q → r))', 'p', '(q → r)', 'q', 'r'],
        hypothesis='p',
        expected=[
            '(p → (q → r))',
            '((p → (q → r)) → ((p → q) → (p → r)))',
            '((p → q) → (p → r))',
            '(q → (p → q))',
            'q',
            '(p → q)',
            '(p → r)'
        ]
    )
)
def test_introduce_conclusion_hypothesis(payload: Sequence[str], hypothesis: str, expected: Sequence[str]) -> None:
    derivation = AxiomaticDerivation(
        axiom_schemas=IMPLICATIONAL_AXIOMS,
        payload=[parse_propositional_formula(s) for s in payload]
    )

    hypothesis_formula = parse_propositional_formula(hypothesis)
    relativized = introduce_conclusion_hypothesis(derivation, hypothesis_formula)
    assert [str(f) for f in relativized.payload] == expected
