import pytest

from ....support.inference import InferenceRuleConnective
from ..common import variables
from ..parsing import parse_term, parse_type, parse_typing_rule, parse_variable_assertion
from ..signature import LambdaSignature
from ..type_system import ExplicitTypeSystem
from ..typing import TypingStyle
from .exceptions import TypeDerivationError, UnknownDerivationRuleError
from .inference import derive_type
from .substitution import substitute
from .tree import apply, assume


def test_substitute_variable_noop(dummy_signature: LambdaSignature) -> None:
    tree = assume(parse_variable_assertion(dummy_signature, 'x: τ'))
    src = variables.y
    dest = assume(parse_variable_assertion(dummy_signature, 'z: τ'))

    assert substitute(tree, variable_mapping={src: dest}) == tree


def test_substitute_incompatible_type(dummy_signature: LambdaSignature) -> None:
    tree = assume(parse_variable_assertion(dummy_signature, 'x: τ'))
    src = variables.x
    dest = assume(parse_variable_assertion(dummy_signature, 'z: σ'))

    with pytest.raises(TypeDerivationError, match='Cannot substitute x: τ for z: σ in x: τ due to incompatible types'):
        substitute(tree, {src: dest})


def test_substitute_variable(dummy_signature: LambdaSignature) -> None:
    tree = assume(parse_variable_assertion(dummy_signature, 'x: τ'))
    src = variables.x
    dest = assume(parse_variable_assertion(dummy_signature, 'y: τ'))

    assert substitute(tree, variable_mapping={src: dest}) == dest


def test_substitute_application(dummy_signature: LambdaSignature) -> None:
    context = {
        variables.x: parse_type(dummy_signature, '(τ → σ)'),
        variables.y: parse_type(dummy_signature, 'τ'),
        variables.z: parse_type(dummy_signature, 'τ')
    }

    tree = derive_type(
        parse_term(dummy_signature, '(xy)', TypingStyle.EXPLICIT),
        context
    )
    src = variables.y
    dest = derive_type(
        parse_term(dummy_signature, 'z', TypingStyle.EXPLICIT),
        context
    )

    expected = derive_type(
        parse_term(dummy_signature, '(xz)', TypingStyle.EXPLICIT),
        context
    )

    assert substitute(tree, {src: dest}) == expected


def test_substitute_abstraction_noop(dummy_signature: LambdaSignature) -> None:
    context = {
            variables.x: parse_type(dummy_signature, 'τ')
    }
    tree = derive_type(
        parse_term(dummy_signature, '(λx:τ.x)', TypingStyle.EXPLICIT)
    )
    src = variables.x
    dest = derive_type(src, context)
    assert substitute(tree, {src: dest}) == tree


def test_substitute_abstraction_renaming(dummy_signature: LambdaSignature) -> None:
    tree = derive_type(
        parse_term(dummy_signature, '(λx:(τ → σ).(xy))', TypingStyle.EXPLICIT),
        {variables.y: parse_type(dummy_signature, 'τ')}
    )
    src = variables.y
    dest = assume(parse_variable_assertion(dummy_signature, 'x: τ'))
    expected = derive_type(
        parse_term(dummy_signature, '(λa:(τ → σ).(ax))', TypingStyle.EXPLICIT),
        {variables.x: parse_type(dummy_signature, 'τ')}
    )

    assert substitute(tree, variable_mapping={src: dest}) == expected


# ex:def:lambda_term_substitution/composed_vs_iterated
def test_substitute_abstraction_renaming_simultaneous(dummy_signature: LambdaSignature) -> None:
    tree = derive_type(
        parse_term(dummy_signature, '(λa:(τ → σ).(xb))', TypingStyle.EXPLICIT),
        {
            variables.x: parse_type(dummy_signature, '(τ → σ)'),
            variables.b: parse_type(dummy_signature, 'τ')
        }
    )
    mapping = {
        variables.x: assume(parse_variable_assertion(dummy_signature, 'a: (τ → σ)')),
        variables.b: assume(parse_variable_assertion(dummy_signature, 'x: τ'))
    }
    expected = derive_type(
        parse_term(dummy_signature, '(λb:(τ → σ).(ax))', TypingStyle.EXPLICIT),
        {
            variables.a: parse_type(dummy_signature, '(τ → σ)'),
            variables.x: parse_type(dummy_signature, 'τ')
        }
    )

    assert substitute(tree, variable_mapping=mapping) == expected


def test_substitute_abstraction_no_renaming(dummy_signature: LambdaSignature) -> None:
    tree = derive_type(
        parse_term(dummy_signature, '(λx:(τ → σ).(xy))', TypingStyle.EXPLICIT),
        {variables.y: parse_type(dummy_signature, 'τ')}
    )
    src = variables.y
    dest = assume(parse_variable_assertion(dummy_signature, 'z: τ'))

    expected = derive_type(
        parse_term(dummy_signature, '(λx:(τ → σ).(xz))', TypingStyle.EXPLICIT),
        {variables.z: parse_type(dummy_signature, 'τ')}
    )

    assert substitute(tree, variable_mapping={src: dest}) == expected


def test_substitute_nested_abstraction_noop(dummy_signature: LambdaSignature) -> None:
    tree = derive_type(
        parse_term(dummy_signature, '(λx:τ.(λy:τ.x))', TypingStyle.EXPLICIT)
    )
    src = variables.y
    dest = assume(parse_variable_assertion(dummy_signature, 'x: τ'))
    assert substitute(tree, {src: dest}) == tree


def test_substitute_unknown_rule() -> None:
    signature = LambdaSignature(constant_terms=['C'], base_types=['τ'])
    system = ExplicitTypeSystem({
        'R': parse_typing_rule(signature, f'{InferenceRuleConnective.SEQUENT} C: τ', TypingStyle.EXPLICIT)
    })

    tree = apply(system, 'R')
    src = variables.x
    dest = assume(parse_variable_assertion(signature, 'y: τ'))

    with pytest.raises(UnknownDerivationRuleError, match='Unknown rule R'):
        substitute(tree, {src: dest})
