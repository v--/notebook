import re
lazy from collections.abc import Mapping

import pytest

from notebook.math.lambda_.arrow_types import derive_type
from notebook.math.lambda_.parsing import parse_type, parse_typed_term, parse_variable
from notebook.math.lambda_.type_context import TypeContext
from notebook.math.lambda_.type_derivation import TypeDerivationError
from notebook.support.pytest import pytest_parametrize_kwargs

from .reduction import reduce_derivation


@pytest_parametrize_kwargs(
    # β−reduction
    dict(
        m='((λx:τ.x)y)',
        n='y',
        context={'y': 'τ'},
    ),
    # β−reduction with α-conversion
    dict(
        m='((λf:(τ → τ).f)(λx:τ.x))',
        n='(λy:τ.y)',
        context={},
    ),
    # β−reduction with nested α-conversion
    dict(
        m='((λf:(τ → τ).f)((λx:(τ → τ).x)(λx:τ.x)))',
        n='((λy:(τ → τ).y)(λy:τ.y))',
        context={},
    ),

    # η−reduction
    dict(
        m='(λx:τ.(fx))',
        n='f',
        context={'f': '(τ → τ)'},
    ),
    # η−reduction with α−conversion
    dict(
        m='(λx:τ.((λy:τ.y)x))',
        n='(λz:τ.z)',
        context={},
    ),
    # η−reduction with deeper α−conversion
    dict(
        m='(λf:τ.(λx:τ.((λy:τ.y)x)))',
        n='(λg:τ.(λz:τ.z))',
        context={},
    ),

    # Only one side of parallel β-reduction
    dict(m='(((λf:(τ → τ).f)g)((λx:τ.x)y))', n='(((λf:(τ → τ).f)g)y)', context={'g': '(τ → τ)', 'y': 'τ'}),
    dict(m='(((λf:(τ → τ).f)g)((λx:τ.x)y))', n='(g((λx:τ.x)y))', context={'g': '(τ → τ)', 'y': 'τ'}),
)
def test_reduce_derivation_success(m: str, n: str, context: Mapping[str, str]) -> None:
    tree = derive_type(
        parse_typed_term(m),
        TypeContext({
            parse_variable(var): parse_type(type_)
            for var, type_ in context.items()
        }),
    )

    reduct = parse_typed_term(n)
    assert reduce_derivation(tree, reduct).conclusion.term == reduct


@pytest_parametrize_kwargs(
    # Reduction is expected, not equal terms
    dict(m='x', n='x', context={'x': 'τ'}),
    dict(m='(fx)', n='(fx)', context={'f': '(τ → τ)', 'x': 'τ'}),
    dict(m='((gx)(fx))', n='((gx)(fx))', context={'g': '(τ → (τ → τ))', 'f': '(τ → τ)', 'x': 'τ'}),
    dict(m='(λx:τ.x)', n='(λx:τ.x)', context={}),

    # α-equivalence is also not sufficient
    dict(m='(λx:τ.x)', n='(λy:τ.y)', context={}),

    # Incompatible types are disallowed
    dict(m='(λx:τ.x)', n='(λx:σ.x)', context={}),
    dict(m='(λx:τ.x)', n='(λx:τ.(λy:σ.x))', context={}),

    # No parallel reduction
    dict(m='(((λf:(τ → τ).f)g)((λx:τ.x)y))', n='(gy)', context={'g': '(τ → τ)', 'y': 'τ'}),
)
def test_reduce_derivation_failure(m: str, n: str, context: Mapping[str, str]) -> None:
    tree = derive_type(
        parse_typed_term(m),
        TypeContext({
            parse_variable(var): parse_type(type_)
            for var, type_ in context.items()
        }),
    )

    reduct = parse_typed_term(n)

    with pytest.raises(TypeDerivationError, match=f'The term {re.escape(m)} is not βη-reducible to {re.escape(n)} in one step'):
        reduce_derivation(tree, reduct)
