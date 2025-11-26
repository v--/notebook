from textwrap import dedent

import pytest

from ....parsing import GreekIdentifier, LatinIdentifier, ParserError, TokenizerError
from ....support.pytest import pytest_parametrize_kwargs, pytest_parametrize_lists
from ..alphabet import BinaryTypeConnective
from ..assertions import TypeAssertion
from ..signature import BaseTypeSymbol, ConstantTermSymbol, LambdaSignature
from ..terms import Constant, TypedAbstraction, UntypedApplication, Variable
from ..types import SimpleConnectiveType, SimpleType, TypeVariable
from .parser import (
    parse_type,
    parse_type_assertion,
    parse_type_variable,
    parse_typed_term,
    parse_typed_term_schema,
    parse_typing_rule,
    parse_untyped_term,
    parse_variable,
)


# This is our base signature from def:hol_signature,
# but with boldface symbols so that the (unicode) symbols do not collide with variables and placeholders
# It is used only for testing the parser.
HOL_TEST_SIGNATURE = LambdaSignature(
    BaseTypeSymbol('𝛊'),
    BaseTypeSymbol('𝐨'),
    ConstantTermSymbol('𝐐')
)


@pytest_parametrize_kwargs(
    dict(
        term='x',
        expected=Variable(LatinIdentifier('x'))
    ),
    dict(
        term='y',
        expected=Variable(LatinIdentifier('y'))
    ),
    dict(
        term='y₁₂',
        expected=Variable(LatinIdentifier('y', index=12))
    )
)
def test_parsing_valid_term_variables(term: str, expected: Variable) -> None:
    assert parse_variable(term) == expected


def test_parsing_accented_variable_name() -> None:
    with pytest.raises(TokenizerError) as excinfo:
        parse_variable('ä')

    assert str(excinfo.value) == 'Unexpected symbol'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ ä
          │ ^
        '''
    )


def test_parsing_long_variable_names() -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_untyped_term('xy')

    assert str(excinfo.value) == 'Finished parsing but there is still input left'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ xy
          │  ^
        '''
    )


def test_parsing_invalid_variable_suffix() -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_untyped_term('x₀₁')

    assert str(excinfo.value) == 'Nonzero subscripts cannot start with zero'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ x₀₁
          │ ^^^
        '''
    )


@pytest_parametrize_kwargs(
    dict(
        term='𝐐',
        expected=Constant('𝐐')
    ),
    dict(
        term='(𝐐(𝐐x))',
        expected=UntypedApplication(
            Constant('𝐐'),
            UntypedApplication(Constant('𝐐'), Variable(LatinIdentifier('x')))
        )
    )
)
def test_parsing_constants(term: str, expected: Constant) -> None:
    assert parse_untyped_term(term, HOL_TEST_SIGNATURE) == expected


@pytest_parametrize_lists(
    term=[
        'x',
        '(xy)',
        '(x₁y₂)',
        '(λx.x)', # I combinator
        '(λx.y)',
        '(λx.(λy.x))', # K combinator
        '(λx.(λy.(λz.((xz)(yz)))))', # S combinator
        '(λf.((λx.(f(xx)))(λx.(f(xx)))))', # Y combinator
    ]
)
def test_rebuilding_terms(term: str) -> None:
    assert str(parse_untyped_term(term)) == term


def test_parsing_abstraction_with_unclosed_parens() -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_untyped_term('(λx.x')

    assert str(excinfo.value) == 'Unclosed parentheses for abstraction'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (λx.x
          │ ^^^^^
        '''
    )


def test_parsing_abstraction_with_unclosed_parens_truncated() -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_untyped_term('(λ')

    assert str(excinfo.value) == 'Expected a variable name after λ'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (λ
          │ ^^
        '''
    )


def test_parsing_abstraction_with_no_dot() -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_untyped_term('(λxx)')

    assert str(excinfo.value) == 'Expected a dot after an abstraction variable'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (λxx)
          │ ^^^^
        '''
    )


def test_parsing_empty_application() -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_untyped_term('()')

    assert str(excinfo.value) == 'Applications must have two terms, while abstractions must begin with λ'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ ()
          │ ^^
        '''
    )


def test_parsing_incomplete_application() -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_untyped_term('(x)')

    assert str(excinfo.value) == 'Applications must have a second subterm'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (x)
          │ ^^^
        '''
    )


@pytest_parametrize_lists(
    term=[
        '(λx.(λy.x))', # K combinator
        '(λx.(λy.(λz.((xz)(yz)))))', # S combinator
        '(λf.((λx.(f(xx)))(λx.(f(xx)))))', # Y combinator
    ]
)
def test_reparsing_terms(term: str) -> None:
    assert str(parse_untyped_term(str(parse_untyped_term(term)))) == term


@pytest_parametrize_kwargs(
    dict(
        term='τ',
        expected=TypeVariable(GreekIdentifier('τ'))
    ),
    dict(
        term='σ',
        expected=TypeVariable(GreekIdentifier('σ'))
    ),
    dict(
        term='τ₁₂',
        expected=TypeVariable(GreekIdentifier('τ', index=12))
    )
)
def test_parsing_valid_type_variables(term: str, expected: TypeVariable) -> None:
    assert parse_type_variable(term) == expected


@pytest_parametrize_lists(
    term=[
        'x',
        '𝐐',
        '(𝐐x)',
        '(λx:𝛊.(𝐐x))',
    ]
)
def test_rebuilding_term_with_constants(term: str) -> None:
    assert str(parse_typed_term(term, HOL_TEST_SIGNATURE)) == term


@pytest_parametrize_lists(
    schema=[
        'x',
        '𝐐', # Constant term
        'M', # Placeholder
        '(QM)',
        '(λx:𝛊.(QM))',
    ]
)
def test_rebuilding_schema(schema: str) -> None:
    assert str(parse_typed_term_schema(schema, HOL_TEST_SIGNATURE)) == schema


def test_parsing_term_schema_with_regular_parser() -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_typed_term('M')

    assert str(excinfo.value) == 'Term placeholders are only allowed in schemas'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ M
          │ ^
        '''
    )


@pytest_parametrize_kwargs(
    dict(
        type_='τ',
        expected=TypeVariable(GreekIdentifier('τ'))
    ),
    dict(
        type_='(τ → σ)',
        expected=SimpleConnectiveType(
            BinaryTypeConnective.ARROW,
            TypeVariable(GreekIdentifier('τ')),
            TypeVariable(GreekIdentifier('σ'))
        )
    ),
    dict(
        type_='(τ × (σ → ρ))',
        expected=SimpleConnectiveType(
            BinaryTypeConnective.PROD,
            TypeVariable(GreekIdentifier('τ')),
            SimpleConnectiveType(
                BinaryTypeConnective.ARROW,
                TypeVariable(GreekIdentifier('σ')),
                TypeVariable(GreekIdentifier('ρ'))
            )
        )
    )
)
def test_parsing_valid_type(type_: str, expected: SimpleType) -> None:
    assert parse_type(type_) == expected


@pytest_parametrize_lists(
    # 𝛊 and 𝐨 are base types, the rest are variables
    # Simply typed higher order logic disallows variables; we only aim to test the parser here
    type_=[
        '𝛊',
        '(𝛊 → 𝐨)',
        'τ',
        '(σ → σ)',
        '(𝛊 → (τ → σ))',
        '((𝛊 → τ) → σ)'
    ]
)
def test_rebuilding_type(type_: str) -> None:
    assert str(parse_type(type_, HOL_TEST_SIGNATURE)) == type_


def test_parsing_type_assertion_missing_arrow() -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_type('(τ σ)')

    assert str(excinfo.value) == 'Binary types must have a connective after the first subtype'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (τ σ)
          │ ^^^^
        '''
    )


def test_parsing_typed_abstraction() -> None:
    var = Variable(LatinIdentifier('x'))
    var_type = TypeVariable(GreekIdentifier('τ'))
    expected = TypedAbstraction(var, var_type, var)
    assert parse_typed_term('(λx:τ.x)') == expected


def test_parsing_typed_abstraction_with_untyped_parser() -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_untyped_term('(λx:τ.x)')

    assert str(excinfo.value) == 'Unexpected type annotation for the abstractor variable in an untyped abstraction'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (λx:τ.x)
          │ ^^^^
        '''
    )


def test_parsing_untyped_abstraction_with_typed_parser() -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_typed_term('(λx.x)')

    assert str(excinfo.value) == 'Expected a type annotation for the abstractor variable in a typed abstraction'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (λx.x)
          │ ^^^^
        '''
    )


@pytest_parametrize_lists(
    assertion=[
        'x: τ',
        'p: (τ → τ)',
        'f: (τ → σ)'
    ]
)
def test_parsing_type_assertion(assertion: str) -> None:
    term, type_ = assertion.split(': ', maxsplit=2)
    expected = TypeAssertion(
        parse_typed_term(term),
        parse_type(type_)
    )

    assert parse_type_assertion(assertion) == expected


def test_parsing_type_assertion_missing_colon() -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_type_assertion('x τ')

    assert str(excinfo.value) == 'Expected a colon after the term in a type specification'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ x τ
          │ ^^^
        '''
    )


@pytest_parametrize_lists(
    rule=[
        '⫢ x: τ',
        'M: (τ → σ), N: τ ⫢ (MN): σ',
        '[x: τ] M: σ ⫢ (λx:τ.M): (τ → σ)'
    ]
)
def test_rebuilding_typing_rules(rule: str) -> None:
    assert parse_typing_rule('name', rule).without_name() == rule


def test_parsing_discharge_schema_with_no_name() -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_typing_rule('name', '[] x: τ ⫢ y: τ')

    assert str(excinfo.value) == 'Empty discharge assumptions are disallowed'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ [] x: τ ⫢ y: τ
          │ ^^
        '''
    )


def test_parsing_discharge_schema_with_no_closing_bracket() -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_typing_rule('name', '[x: τ y: τ ⫢ z: τ')

    assert str(excinfo.value) == 'Unclosed bracket for discharge schema'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ [x: τ y: τ ⫢ z: τ
          │ ^^^^^
        '''
    )
