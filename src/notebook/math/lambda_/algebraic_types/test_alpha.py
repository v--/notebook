import re
from typing import TYPE_CHECKING

import pytest

from notebook.math.lambda_.algebraic_types import SIMPLE_ALGEBRAIC_SIGNATURE, SIMPLE_ALGEBRAIC_TYPE_SYSTEM
from notebook.math.lambda_.arrow_types import derive_type
from notebook.math.lambda_.assertions import VariableTypeAssertion
from notebook.math.lambda_.instantiation import AtomicLambdaSchemaInstantiation
from notebook.math.lambda_.parsing import (
    parse_type,
    parse_type_placeholder,
    parse_typed_term,
    parse_variable,
    parse_variable_assertion,
)
from notebook.math.lambda_.signature import BaseTypeSymbol
from notebook.math.lambda_.type_context import TypeContext
from notebook.math.lambda_.type_derivation import (
    RuleApplicationTree,
    TypeDerivationError,
    apply,
    assume,
    premise_config,
)
from notebook.math.lambda_.types import BaseType
from notebook.support.pytest import pytest_parametrize_kwargs

from .alpha import alpha_convert_derivation


if TYPE_CHECKING:
    from collections.abc import Mapping


@pytest_parametrize_kwargs(
    dict(m='x', n='x', context={'x': 'τ'}),
    dict(m='(fx)', n='(fx)', context={'f': '(τ → τ)', 'x': 'τ'}),
    dict(m='(λx:τ.x)', n='(λx:τ.x)', context={}),
    dict(m='(λx:τ.x)', n='(λy:τ.y)', context={}),
    dict(
        m='(λx:(τ → σ).(λy:τ.(xy)))',
        n='(λa:(τ → σ).(λb:τ.(ab)))',
        context={},
    ),
)
def test_alpha_convert_arrow_derivation_success(m: str, n: str, context: Mapping[str, str]) -> None:
    tree = derive_type(
        parse_typed_term(m),
        TypeContext({
            parse_variable(var): parse_type(type_)
            for var, type_ in context.items()
        }),
    )

    equivalent_term = parse_typed_term(n)
    assert alpha_convert_derivation(tree, equivalent_term).conclusion.term == equivalent_term


@pytest_parametrize_kwargs(
    dict(m='x', n='y', context={'x': 'τ'}),
    dict(m='(λx:τ.x)', n='(λx:σ.x)', context={}),
    dict(m='(λx:τ.x)', n='(λx:τ.y)', context={}),
    dict(
        m='(λx:(τ → σ).(λy:τ.(xy)))',
        n='(λa:(τ → σ).(λa:τ.(aa)))',
        context={},
    ),
)
def test_alpha_convert_arrow_derivation_failure(m: str, n: str, context: Mapping[str, str]) -> None:
    tree = derive_type(
        parse_typed_term(m),
        TypeContext({
            parse_variable(var): parse_type(type_)
            for var, type_ in context.items()
        }),
    )

    equivalent_term = parse_typed_term(n)

    with pytest.raises(TypeDerivationError, match=f'The terms {re.escape(m)} and {re.escape(n)} are not α-equivalent'):
        alpha_convert_derivation(tree, equivalent_term)


def test_alpha_convert_sum_elim() -> None:
    def factory(x: str, y: str) -> RuleApplicationTree:
        return apply(
            SIMPLE_ALGEBRAIC_TYPE_SYSTEM['+₋'],

            apply(
                SIMPLE_ALGEBRAIC_TYPE_SYSTEM['+₊ₗ'],
                assume(parse_variable_assertion('x: 𝟙', SIMPLE_ALGEBRAIC_SIGNATURE)),
                instantiation=AtomicLambdaSchemaInstantiation(
                    type_mapping={
                        parse_type_placeholder('σ'): parse_type('σ'),
                    },
                ),
            ),

            premise_config(
                tree=assume(VariableTypeAssertion(parse_variable(x), BaseType(BaseTypeSymbol('𝟙')))),
                attachments=[VariableTypeAssertion(parse_variable(x), BaseType(BaseTypeSymbol('𝟙')))],
            ),

            premise_config(
                tree=apply(SIMPLE_ALGEBRAIC_TYPE_SYSTEM['𝟙₊']),
                attachments=[VariableTypeAssertion(parse_variable(y), parse_type('σ'))],
            ),
        )

    tree = factory(x='a', y='b')
    equivalent_term = parse_typed_term('(((S₋(λc:𝟙.c))(λd:σ.U₊))(S₊ₗx))', SIMPLE_ALGEBRAIC_SIGNATURE)
    expected = factory(x='c', y='d')

    assert alpha_convert_derivation(tree, equivalent_term) == expected
