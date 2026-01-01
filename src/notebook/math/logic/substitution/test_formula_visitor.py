from collections.abc import Mapping

from ....support.pytest import pytest_parametrize_kwargs
from ..parsing import parse_formula, parse_term, parse_variable
from ..signature import FormalLogicSignature
from .formula_visitor import substitute_in_formula


@pytest_parametrize_kwargs(
    # Straighforward substitution
    dict(
        formula='p¹(x)',
        mapping=dict(x='y'),
        expected='p¹(y)'
    ),
    dict(
        formula='p¹(y)',
        mapping=dict(x='z'),
        expected='p¹(y)'
    ),
    # (Avoiding) capturing free variables
    dict(
        formula='∀x.p¹(y)',
        mapping=dict(y='z'),
        expected='∀x.p¹(z)'
    ),
    dict(
        formula='∀x.p¹(y)',
        mapping=dict(y='x'),
        expected='∀a.p¹(x)'
    ),
    dict(
        formula='∀x.p²(x, y)',
        mapping=dict(y='x'),
        expected='∀a.p²(a, x)'
    ),
    dict(
        formula='∀x.p³(x, y, z)',
        mapping=dict(y='z', z='y'),
        expected='∀x.p³(x, z, y)'
    ),
    dict(
        formula='∀x.p³(x, y, z)',
        mapping=dict(y='x', z='a'),
        expected='∀b.p³(b, x, a)'
    ),
    # (Avoiding) colliding variables
    dict(
        formula='∀x.p¹(y)',
        mapping=dict(y='x'),
        expected='∀a.p¹(x)'
    ),
)
def test_substitute_in_formula(
    formula: str,
    mapping: Mapping[str, str],
    expected: str,
    dummy_signature: FormalLogicSignature
) -> None:
    formula_ = parse_formula(formula, dummy_signature)
    expected_ = parse_formula(expected, dummy_signature)
    result = substitute_in_formula(
        formula_,
        {parse_variable(key): parse_term(value, dummy_signature) for key, value in mapping.items()}
    )

    assert result == expected_
