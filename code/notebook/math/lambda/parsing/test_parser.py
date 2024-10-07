from textwrap import dedent

import pytest

from ....parsing.identifiers import LatinIdentifier
from ....parsing.parser import ParsingError
from ....support.pytest import pytest_parametrize_kwargs, pytest_parametrize_lists
from ..terms import Variable
from .parser import parse_term


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
    assert parse_term(term) == expected


def test_parsing_long_variable_names() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_term('xy')

    assert str(excinfo.value) == 'Finished parsing but there is still input left'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ xy
          │  ^
        '''
    )


def test_parsing_invalid_variable_suffix() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_term('x₀₁')

    assert str(excinfo.value) == 'Nonzero natural numbers cannot start with zero'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ x₀₁
          │  ^^
        '''
    )


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
    assert str(parse_term(term)) == term


def test_parsing_abstraction_with_unclosed_parens() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_term('(λx.x')

    assert str(excinfo.value) == 'Unclosed parentheses for abstraction'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (λx.x
          │ ^^^^^
        '''
    )


def test_parsing_abstraction_with_unclosed_parens_truncated() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_term('(λ')

    assert str(excinfo.value) == 'Expected a variable name after λ'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (λ
          │ ^^
        '''
    )


def test_parsing_abstraction_with_no_dot() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_term('(λxx)')

    assert str(excinfo.value) == 'Expected a dot after an abstraction variable'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (λxx)
          │ ^^^^
        '''
    )


def test_parsing_empty_application() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_term('()')

    assert str(excinfo.value) == 'Applications must have two terms, while abstractions must begin with λ'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ ()
          │ ^^
        '''
    )


def test_parsing_incomplete_application() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_term('(x)')

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
    assert str(parse_term(str(parse_term(term)))) == term
