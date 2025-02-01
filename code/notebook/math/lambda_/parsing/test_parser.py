from textwrap import dedent

import pytest

from ....parsing.identifiers import LatinIdentifier
from ....parsing.parser import ParsingError
from ....support.pytest import pytest_parametrize_kwargs, pytest_parametrize_lists
from ..assertions import TypeAssertion
from ..terms import Application, Constant, Variable
from ..type_systems import ANDREWS_HOL_SIGNATURE
from .parser import (
    parse_pure_term,
    parse_term,
    parse_term_schema,
    parse_type,
    parse_type_assertion,
    parse_type_schema,
    parse_typing_rule,
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
def test_parsing_valid_variables(term: str, expected: Variable) -> None:
    assert parse_pure_term(term) == expected


def test_parsing_long_variable_names() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_pure_term('xy')

    assert str(excinfo.value) == 'Finished parsing but there is still input left'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ xy
          │  ^
        '''
    )


def test_parsing_invalid_variable_suffix() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_pure_term('x₀₁')

    assert str(excinfo.value) == 'Nonzero natural numbers cannot start with zero'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ x₀₁
          │  ^^
        '''
    )


@pytest_parametrize_kwargs(
    dict(
        term='Q',
        expected=Constant('Q')
    ),
    dict(
        term='(I(Qx))',
        expected=Application(Constant('I'), Application(Constant('Q'), Variable(LatinIdentifier('x'))))
    )
)
def test_parsing_constants(term: str, expected: Variable) -> None:
    assert parse_term(ANDREWS_HOL_SIGNATURE, term) == expected


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
    assert str(parse_pure_term(term)) == term


def test_parsing_abstraction_with_unclosed_parens() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_pure_term('(λx.x')

    assert str(excinfo.value) == 'Unclosed parentheses for abstraction'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (λx.x
          │ ^^^^^
        '''
    )


def test_parsing_abstraction_with_unclosed_parens_truncated() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_pure_term('(λ')

    assert str(excinfo.value) == 'Expected a variable name after λ'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (λ
          │ ^^
        '''
    )


def test_parsing_abstraction_with_no_dot() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_pure_term('(λxx)')

    assert str(excinfo.value) == 'Expected a dot after an abstraction variable'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (λxx)
          │ ^^^^
        '''
    )


def test_parsing_empty_application() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_pure_term('()')

    assert str(excinfo.value) == 'Applications must have two terms, while abstractions must begin with λ'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ ()
          │ ^^
        '''
    )


def test_parsing_incomplete_application() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_pure_term('(x)')

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
    assert str(parse_pure_term(str(parse_pure_term(term)))) == term


@pytest_parametrize_lists(
    term=[
        'x',
        'Q',
        '(Qx)',
        '(λx.(Qx))',
    ]
)
def test_rebuilding_term_with_constants(term: str) -> None:
    assert str(parse_term(ANDREWS_HOL_SIGNATURE, term)) == term


@pytest_parametrize_lists(
    schema=[
        'x',
        'Q', # Constant
        'M', # Placeholder
        '(QM)',
        '(λx.(QM))',
    ]
)
def test_rebuilding_schema(schema: str) -> None:
    assert str(parse_term_schema(ANDREWS_HOL_SIGNATURE, schema)) == schema


def test_parsing_term_schema_with_regular_parser() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_pure_term('M')

    assert str(excinfo.value) == 'Term placeholders are only allowed in schemas'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ M
          │ ^
        '''
    )


@pytest_parametrize_lists(
    # ι and o are base types, the rest are placeholders
    schema=[
        'ι',
        '(ι → o)',
        'α',
        '(α → β)',
        '(o → (α → β))',
        '((o → α) → β)',
    ]
)
def test_rebuilding_type_schema(schema: str) -> None:
    assert str(parse_type_schema(ANDREWS_HOL_SIGNATURE, schema)) == schema


def test_parsing_type_schema_with_regular_parser() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_type(ANDREWS_HOL_SIGNATURE, 'α')

    assert str(excinfo.value) == 'Type placeholders are only allowed in schemas'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ α
          │ ^
        '''
    )


def test_parsing_type_assertion_missing_arrow() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_type(ANDREWS_HOL_SIGNATURE, '(ι o)')

    assert str(excinfo.value) == 'Expected an arrow connecting type specifications'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (ι o)
          │ ^^^^
        '''
    )


@pytest_parametrize_lists(
    assertion=[
        'x: ι',
        'p: (ι → ι)',
        'f: (ι → o)'
    ]
)
def test_parsing_type_assertion(assertion: str) -> None:
    term, type_ = assertion.split(': ', maxsplit=2)
    expected = TypeAssertion(
        parse_term(ANDREWS_HOL_SIGNATURE, term),
        parse_type(ANDREWS_HOL_SIGNATURE, type_)
    )

    assert parse_type_assertion(ANDREWS_HOL_SIGNATURE, assertion) == expected


def test_parsing_type_assertion_missing_colon() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_type_assertion(ANDREWS_HOL_SIGNATURE, 'x ι')

    assert str(excinfo.value) == 'Expected a colon after the term in a type specification'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ x ι
          │ ^^
        '''
    )


@pytest_parametrize_lists(
    rule=[
        '(R) ⫢ x: ι',
        '(R) M: (α → β), N: α ⫢ (MN): β',
        '(R) [x: α] M: β ⫢ (λx.M): (α → β)'
    ]
)
def test_rebuilding_typing_rules(rule: str) -> None:
    assert str(parse_typing_rule(ANDREWS_HOL_SIGNATURE, rule)) == rule


def test_parsing_discharge_schema_with_no_name() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_typing_rule(ANDREWS_HOL_SIGNATURE, '(R) [] x: ι ⫢ y: ι')

    assert str(excinfo.value) == 'Unexpected token'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (R) [] x: ι ⫢ y: ι
          │      ^
        '''
    )


def test_parsing_discharge_schema_with_no_closing_bracket() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_typing_rule(ANDREWS_HOL_SIGNATURE, '(R) [x: ι y: ι ⫢ z: ι')

    assert str(excinfo.value) == 'Unclosed bracket for discharge schema'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (R) [x: ι y: ι ⫢ z: ι
          │     ^^^^^^
        '''
    )
