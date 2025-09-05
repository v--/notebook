import re

import pytest

from ....support.inference import InferenceRuleConnective
from ..arrow_types import derive_type
from ..common import variables
from ..instantiation import LambdaSchemaInstantiation
from ..parsing import (
    parse_type,
    parse_type_placeholder,
    parse_typed_term,
    parse_typing_rule,
    parse_variable_assertion,
)
from ..signature import LambdaSignature
from ..type_derivation import TypeDerivationError, UnknownDerivationRuleError, apply, assume, premise
from .substitution import substitute_in_tree
from .system import SIMPLE_ALGEBRAIC_SIGNATURE, SIMPLE_ALGEBRAIC_TYPE_SYSTEM


def test_substitute_variable_noop() -> None:
    tree = assume(parse_variable_assertion('x: τ'))
    src = variables.y
    dest = assume(parse_variable_assertion('z: τ'))

    assert substitute_in_tree(tree, variable_mapping={src: dest}) == tree


def test_substitute_incompatible_type() -> None:
    tree = assume(parse_variable_assertion('x: τ'))
    src = variables.x
    dest = assume(parse_variable_assertion('z: σ'))

    with pytest.raises(TypeDerivationError, match='Cannot substitute x: τ for z: σ in x: τ due to incompatible types'):
        substitute_in_tree(tree, {src: dest})


def test_substitute_variable() -> None:
    tree = assume(parse_variable_assertion('x: τ'))
    src = variables.x
    dest = assume(parse_variable_assertion('y: τ'))

    assert substitute_in_tree(tree, variable_mapping={src: dest}) == dest


def test_substitute_application() -> None:
    context = {
        variables.x: parse_type('(τ → σ)'),
        variables.y: parse_type('τ'),
        variables.z: parse_type('τ')
    }

    tree = derive_type(
        parse_typed_term('(xy)'),
        context
    )
    src = variables.y
    dest = derive_type(
        parse_typed_term('z'),
        context
    )

    expected = derive_type(
        parse_typed_term('(xz)'),
        context
    )

    assert substitute_in_tree(tree, {src: dest}) == expected


def test_substitute_abstraction_noop() -> None:
    context = {
        variables.x: parse_type('τ')
    }
    tree = derive_type(
        parse_typed_term('(λx:τ.x)')
    )
    src = variables.x
    dest = derive_type(src, context)
    assert substitute_in_tree(tree, {src: dest}) == tree


def test_substitute_abstraction_renaming() -> None:
    tree = derive_type(
        parse_typed_term('(λx:(τ → σ).(xy))'),
        {variables.y: parse_type('τ')}
    )
    src = variables.y
    dest = assume(parse_variable_assertion('x: τ'))
    expected = derive_type(
        parse_typed_term('(λa:(τ → σ).(ax))'),
        {variables.x: parse_type('τ')}
    )

    assert substitute_in_tree(tree, variable_mapping={src: dest}) == expected


# ex:def:lambda_term_substitution/composed_vs_iterated
def test_substitute_abstraction_renaming_simultaneous() -> None:
    tree = derive_type(
        parse_typed_term('(λa:(τ → σ).(xb))'),
        {
            variables.x: parse_type('(τ → σ)'),
            variables.b: parse_type('τ')
        }
    )
    mapping = {
        variables.x: assume(parse_variable_assertion('a: (τ → σ)')),
        variables.b: assume(parse_variable_assertion('x: τ'))
    }
    expected = derive_type(
        parse_typed_term('(λb:(τ → σ).(ax))'),
        {
            variables.a: parse_type('(τ → σ)'),
            variables.x: parse_type('τ')
        }
    )

    assert substitute_in_tree(tree, variable_mapping=mapping) == expected


def test_substitute_abstraction_no_renaming() -> None:
    tree = derive_type(
        parse_typed_term('(λx:(τ → σ).(xy))'),
        {variables.y: parse_type('τ')}
    )
    src = variables.y
    dest = assume(parse_variable_assertion('z: τ'))

    expected = derive_type(
        parse_typed_term('(λx:(τ → σ).(xz))'),
        {variables.z: parse_type('τ')}
    )

    assert substitute_in_tree(tree, variable_mapping={src: dest}) == expected


def test_substitute_nested_abstraction_noop() -> None:
    tree = derive_type(
        parse_typed_term('(λx:τ.(λy:τ.x))')
    )
    src = variables.y
    dest = assume(parse_variable_assertion('x: τ'))
    assert substitute_in_tree(tree, {src: dest}) == tree


def test_substitute_unknown_rule() -> None:
    signature = LambdaSignature(constant_terms=['C'], base_types=['T'])
    rule = parse_typing_rule('R', f'{InferenceRuleConnective.SEQUENT} C: T', signature)
    tree = apply(rule)
    src = variables.x
    dest = assume(parse_variable_assertion('y: T', signature))

    with pytest.raises(UnknownDerivationRuleError, match=re.escape("Unrecognized inference rule '(R) ⫢ C: T'")):
        substitute_in_tree(tree, {src: dest})


# Analogous to the previous test, but with a rule name that collides with an arrow type rule
def test_substitute_unknown_rule_with_matching_name() -> None:
    signature = LambdaSignature(constant_terms=['C'], base_types=['T'])
    rule = parse_typing_rule('→₊', f'{InferenceRuleConnective.SEQUENT} C: T', signature)
    tree = apply(rule)
    src = variables.x
    dest = assume(parse_variable_assertion('y: T', signature))

    with pytest.raises(UnknownDerivationRuleError, match=re.escape("Unrecognized inference rule '(→₊) ⫢ C: T'")):
        substitute_in_tree(tree, {src: dest})


def test_substitute_top_intro_noop() -> None:
    tree = apply(SIMPLE_ALGEBRAIC_TYPE_SYSTEM['1₊'])
    src = variables.x
    dest = assume(parse_variable_assertion('x: 0', SIMPLE_ALGEBRAIC_SIGNATURE))

    assert substitute_in_tree(tree, {src: dest}) == tree


def test_substitute_bot_elim() -> None:
    tree = apply(
        SIMPLE_ALGEBRAIC_TYPE_SYSTEM['0₋'],
        assume(
            parse_variable_assertion('x: 0', SIMPLE_ALGEBRAIC_SIGNATURE),
        ),
        instantiation=LambdaSchemaInstantiation(
            type_mapping={
                parse_type_placeholder('τ'): parse_type('τ', SIMPLE_ALGEBRAIC_SIGNATURE)
            }
        )
    )

    src = variables.x
    dest = assume(parse_variable_assertion('y: 0', SIMPLE_ALGEBRAIC_SIGNATURE))

    expected = apply(
        SIMPLE_ALGEBRAIC_TYPE_SYSTEM['0₋'],
        dest,
        instantiation=LambdaSchemaInstantiation(
            type_mapping={
                parse_type_placeholder('τ'): parse_type('τ', SIMPLE_ALGEBRAIC_SIGNATURE)
            }
        )
    )

    assert substitute_in_tree(tree, {src: dest}) == expected


def test_substitute_sum_elim_without_renaming() -> None:
    tree = apply(
        SIMPLE_ALGEBRAIC_TYPE_SYSTEM['+₋'],

        apply(
            SIMPLE_ALGEBRAIC_TYPE_SYSTEM['+₊ₗ'],
            assume(parse_variable_assertion('x: 1', SIMPLE_ALGEBRAIC_SIGNATURE)),
            instantiation=LambdaSchemaInstantiation(
                type_mapping={
                    parse_type_placeholder('σ'): parse_type('σ')
                }
            )
        ),

        premise(
            tree=assume(parse_variable_assertion('a: 1', SIMPLE_ALGEBRAIC_SIGNATURE)),
            discharge=parse_variable_assertion('y: 1', SIMPLE_ALGEBRAIC_SIGNATURE)
        ),

        premise(
            tree=apply(SIMPLE_ALGEBRAIC_TYPE_SYSTEM['1₊']),
            discharge=parse_variable_assertion('z: σ', SIMPLE_ALGEBRAIC_SIGNATURE)
        )
    )

    # "a" gets replaced with "y", and due to renaming "y" gets replaced with "a"
    src = variables.a
    dest = assume(parse_variable_assertion('y: 1', SIMPLE_ALGEBRAIC_SIGNATURE))

    expected = apply(
        SIMPLE_ALGEBRAIC_TYPE_SYSTEM['+₋'],

        apply(
            SIMPLE_ALGEBRAIC_TYPE_SYSTEM['+₊ₗ'],
            assume(parse_variable_assertion('x: 1', SIMPLE_ALGEBRAIC_SIGNATURE)),
            instantiation=LambdaSchemaInstantiation(
                type_mapping={
                    parse_type_placeholder('σ'): parse_type('σ')
                }
            )
        ),

        premise(
            tree=assume(parse_variable_assertion('y: 1', SIMPLE_ALGEBRAIC_SIGNATURE)),
            discharge=parse_variable_assertion('a: 1', SIMPLE_ALGEBRAIC_SIGNATURE)
        ),

        premise(
            tree=apply(SIMPLE_ALGEBRAIC_TYPE_SYSTEM['1₊']),
            discharge=parse_variable_assertion('z: σ', SIMPLE_ALGEBRAIC_SIGNATURE)
        )
    )

    assert substitute_in_tree(tree, variable_mapping={src: dest}) == expected
