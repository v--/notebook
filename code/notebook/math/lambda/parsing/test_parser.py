import pytest

from ....parsing.parser import ParsingError
from ..terms import Variable
from .parser import parse_term


def test_parsing_variables_valid():
    assert parse_term('x') == Variable('x')
    assert parse_term('y') == Variable('y')
    assert parse_term('z₁₂') == Variable('z₁₂')


def test_parsing_variables_invalid():
    # Only one letter per variable
    with pytest.raises(ParsingError):
        parse_term('xy')

    # Disallow leading zeros
    with pytest.raises(ParsingError):
        parse_term('x₀₁')

    # And no trailing characters
    with pytest.raises(ParsingError):
        parse_term('x ')


def test_parsing_terms_valid():
    def is_term_rebuilt(string: str):
        assert str(parse_term(string)) == string

    is_term_rebuilt('x')
    is_term_rebuilt('(xy)')
    is_term_rebuilt('(x₁y₂)')
    is_term_rebuilt('(λx.x)') # I combinator
    is_term_rebuilt('(λx.y)')

    is_term_rebuilt('(λx.(λy.x))') # K combinator
    is_term_rebuilt('(λx.(λy.(λz.((xz)(yz)))))') # S combinator
    is_term_rebuilt('(λf.((λx.(f(xx)))(λx.(f(xx)))))') # Y combinator


def test_parsing_abstraction_invalid():
    with pytest.raises(ParsingError):
        parse_term('(λ')

    with pytest.raises(ParsingError):
        parse_term('(λx')

    with pytest.raises(ParsingError):
        parse_term('(λx.')

    with pytest.raises(ParsingError):
        parse_term('(λx.x')


def test_parsing_application_invalid():
    with pytest.raises(ParsingError):
        parse_term('(')

    with pytest.raises(ParsingError):
        parse_term('(x')

    with pytest.raises(ParsingError):
        parse_term('(xy')


def test_reparsing_terms():
    def is_term_rebuilt(string: str):
        assert str(parse_term(str(parse_term(string)))) == string

    is_term_rebuilt('(λx.(λy.x))') # K combinator
    is_term_rebuilt('(λx.(λy.(λz.((xz)(yz)))))') # S combinator
    is_term_rebuilt('(λf.((λx.(f(xx)))(λx.(f(xx)))))') # Y combinator
