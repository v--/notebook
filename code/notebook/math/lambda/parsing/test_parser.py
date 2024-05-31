from textwrap import dedent

import pytest

from ....parsing.identifiers import LatinIdentifier
from ....parsing.parser import ParsingError
from ..terms import Variable
from .parser import parse_term


def test_parsing_valid_variables() -> None:
    assert parse_term('x') == Variable(LatinIdentifier('x'))
    assert parse_term('y') == Variable(LatinIdentifier('y'))
    assert parse_term('z₁₂') == Variable(LatinIdentifier('z', index=12))


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


def test_parsing_valid_terms() -> None:
    def is_term_rebuilt(string: str) -> None:
        assert str(parse_term(string)) == string

    is_term_rebuilt('x')
    is_term_rebuilt('(xy)')
    is_term_rebuilt('(x₁y₂)')
    is_term_rebuilt('(λx.x)') # I combinator
    is_term_rebuilt('(λx.y)')

    is_term_rebuilt('(λx.(λy.x))') # K combinator
    is_term_rebuilt('(λx.(λy.(λz.((xz)(yz)))))') # S combinator
    is_term_rebuilt('(λf.((λx.(f(xx)))(λx.(f(xx)))))') # Y combinator


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


def test_reparsing_terms() -> None:
    def is_term_rebuilt(string: str) -> None:
        assert str(parse_term(str(parse_term(string)))) == string

    is_term_rebuilt('(λx.(λy.x))') # K combinator
    is_term_rebuilt('(λx.(λy.(λz.((xz)(yz)))))') # S combinator
    is_term_rebuilt('(λf.((λx.(f(xx)))(λx.(f(xx)))))') # Y combinator
