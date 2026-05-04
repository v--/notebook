from typing import TYPE_CHECKING

from notebook.math.lambda_.parsing import parse_untyped_term, parse_variable
from notebook.support.coderefs import collector
from notebook.support.pytest import pytest_parametrize_kwargs

from .substitution import substitute


if TYPE_CHECKING:
    from collections.abc import Mapping


@pytest_parametrize_kwargs(
    # Variables and applications
    dict(
        term='x',
        mapping=dict(x='y'),
        expected='y',
    ),
    dict(
        term='z',
        mapping=dict(x='y'),
        expected='z',
    ),
    dict(
        term='(xy)',
        mapping=dict(x='y'),
        expected='(yy)',
    ),

    # Multiple replacements in abstractions
    collector.ref_proxy('ex:alg:lambda_term_substitution/simultaneous',
        term='(λx.((xy)z))',
        mapping=dict(x='a', y='b', z='c'),
        expected='(λx.((xb)c))',
    ),

    # Combinators should remain unchanged
    collector.ref_proxy('ex:alg:lambda_term_substitution/nested_noop',
        term='(λx.x)',
        mapping=dict(y='x'),
        expected='(λx.x)',
    ),
    dict(
        term='(λx.(λy.(yx)))',
        mapping=dict(y='x'),
        expected='(λx.(λy.(yx)))',
    ),

    # Renaming
    collector.ref_proxy('ex:alg:lambda_term_substitution/capture',
        term='(λx.(xy))',
        mapping=dict(y='x'),
        expected='(λa.(ax))',
    ),
    collector.ref_proxy('ex:alg:lambda_term_substitution/ignoring',
        term='(λx.(xy))',
        mapping=dict(y='z'),
        expected='(λx.(xz))',
    ),
    collector.ref_proxy('ex:alg:lambda_term_substitution/composed_vs_iterated',
        term='(λa.(xb))',
        mapping=dict(x='a', b='x'),
        expected='(λb.(ax))',
    ),
    dict(
        term='(λa.(xb))',
        mapping=dict(x='a'),
        expected='(λc.(ab))',
    ),
    collector.ref_proxy('thm:lambda_substitutions_agree',
        term='(λx.(xy))',
        mapping=dict(y='x'),
        expected='(λa.(ax))',
    ),
    dict(
        term='(λx.(xy))',
        # Specifying how to substitute bound variables should not affect the result since we override the specification.
        # In particular, the substituted value of x does not affect the choice of fresh variables.
        mapping=dict(y='x', x='a'),
        expected='(λa.(ax))',
    ),
)
def test_substitute_in_term(term: str, mapping: Mapping[str, str], expected: str) -> None:
    sub = substitute(
        parse_untyped_term(term),
        {parse_variable(key): parse_untyped_term(value) for key, value in mapping.items()},
    )

    assert str(sub) == expected
