from collections.abc import Mapping

from ....support.pytest import pytest_parametrize_kwargs
from ..parsing import parse_term, parse_variable
from ..signature import FormalLogicSignature
from .term_visitor import substitute_in_term


@pytest_parametrize_kwargs(
    dict(
        term='x',
        mapping=dict(x='y'),
        expected='y'
    ),
    dict(
        term='y',
        mapping=dict(x='z'),
        expected='y'
    ),
    dict(
        term='f¹(x)',
        mapping=dict(x='y'),
        expected='f¹(y)'
    ),
    dict(
        term='f²(g¹(x), y)',
        mapping=dict(x='y', y='x'),
        expected='f²(g¹(y), x)'
    )
)
def test_substitute_in_term(
    term: str,
    mapping: Mapping[str, str],
    expected: str,
    dummy_signature: FormalLogicSignature
) -> None:
    term_ = parse_term(term, dummy_signature)
    expected_ = parse_term(expected, dummy_signature)

    result = substitute_in_term(
        term_,
        {parse_variable(key): parse_term(value, dummy_signature) for key, value in mapping.items()}
    )

    assert result == expected_
