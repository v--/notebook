from ...support.pytest import pytest_parametrize_kwargs
from .parsing import parse_term, parse_variable
from .substitution import Substitution, apply_substitution


@pytest_parametrize_kwargs(
    # Variables and applications
    dict(
        term='x',
        mapping=dict(x='y'),
        expected='y'
    ),
    dict(
        term='z',
        mapping=dict(x='y'),
        expected='z'
    ),
    dict(
        term='(xy)',
        mapping=dict(x='y'),
        expected='(yy)'
    ),

    # Multiple replacements in abstractions
    ## ex:def:lambda_substitution/simultaneous
    dict(
        term='(λx.((xy)z))',
        mapping=dict(x='a', y='b', z='c'),
        expected='(λx.((xb)c))'
    ),

    # Combinators should remain unchanged
    ## ex:def:lambda_substitution/nested_noop
    dict(
        term='(λx.x)',
        mapping=dict(y='x'),
        expected='(λx.x)'
    ),
    dict(
        term='(λx.(λy.(yx)))',
        mapping=dict(y='x'),
        expected='(λx.(λy.(yx)))'
    ),

    # Renaming
    ## ex:def:lambda_substitution/capture
    dict(
        term='(λx.(xy))',
        mapping=dict(y='x'),
        expected='(λa.(ax))'
    ),
    ## ex:def:lambda_substitution/ignoring
    dict(
        term='(λx.(xy))',
        mapping=dict(y='z'),
        expected='(λx.(xz))'
    ),
)
def test_substitute_in_term(term: str,
    mapping: dict[str, str],
    expected: str) -> None:
    sub = apply_substitution(
        parse_term(term),
        Substitution({ parse_variable(key): parse_term(value) for key, value in
            mapping.items() })
    )

    assert str(sub) == expected
