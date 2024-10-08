from textwrap import dedent

import pytest

from ....parsing.parser import ParsingError
from ....support.pytest import pytest_parametrize_lists
from .parser import parse_rule


@pytest_parametrize_lists(
    rule=[
        '(R) ⫢ ψ',
        '(R) φ ⫢ ψ',
        '(R) φ₁, φ₂ ⫢ ψ'
    ]
)
def test_rebuilding_rules(rule: str) -> None:
    assert str(parse_rule(rule)) == rule


def test_parsing_without_rule_name() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_rule('φ ⫢ ψ')

    assert str(excinfo.value) == 'A rule must start with a parenthesized name'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ φ ⫢ ψ
          │ ^
        '''
    )


def test_parsing_with_empty_name() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_rule('() φ ⫢ ψ')

    assert str(excinfo.value) == 'The name of a rule cannot be empty'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ () φ ⫢ ψ
          │ ^^
        '''
    )


def test_parsing_rule_with_unclosed_parens() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_rule('(R φ ⫢ ψ')

    assert str(excinfo.value) == 'Unclosed parenthesis after rule name'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (R φ ⫢ ψ
          │ ^^^
        '''
    )


def test_parsing_rule_with_no_comma() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_rule('(R) φ₁ φ₂ ⫢ ψ')

    assert str(excinfo.value) == 'Expected either a comma or a sequent symbol after a schema'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (R) φ₁ φ₂ ⫢ ψ
          │        ^^
        '''
    )


def test_parsing_rule_with_no_conclusion() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_rule('(R) φ')

    assert str(excinfo.value) == 'Expected a sequent symbol'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (R) φ
          │     ^
        '''
    )


def test_parsing_valid_discharge_schemas() -> None:
    def assert_rule_rebuilt(string: str) -> None:
        assert str(parse_rule(string)) == string

    assert_rule_rebuilt('(R) [θ] φ ⫢ ψ')


def test_parsing_discharge_schema_with_no_name() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_rule('(R) [] φ ⫢ ψ')

    assert str(excinfo.value) == 'Unexpected token'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (R) [] φ ⫢ ψ
          │      ^
        '''
    )


def test_parsing_discharge_schema_with_no_closing_bracket() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_rule('(R) [θ φ ⫢ ψ')

    assert str(excinfo.value) == 'Unclosed brackets for discharge schemas'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (R) [θ φ ⫢ ψ
          │     ^^^
        '''
    )


def test_parsing_discharge_in_conclusion() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_rule('(R) ⫢ [θ] ψ')

    assert str(excinfo.value) == 'The conclusion cannot have a discharge schema'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (R) ⫢ [θ] ψ
          │       ^^^^^
        '''
    )


@pytest_parametrize_lists(
    rule=[
        '(R) ⫢ ⊥',
        '(R) φ ⫢ ¬ψ',
        '(R) ⫢ (ψ₁ ∧ ψ₂)',
        '(R) ⫢ ∀x.ψ'
    ]
)
def test_rebuilding_complex_rules(rule: str) -> None:
    assert str(parse_rule(rule)) == rule


# The quantifier parser is an almost literal copy of the one from the FOL parser, so we rely on the tests there
def test_parsing_quantifier_schema_with_no_dot() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_rule('(R) ⫢ ∀xψ')

    assert str(excinfo.value) == 'Expected dot after variable'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (R) ⫢ ∀xψ
          │       ^^^
    ''')


# The same goes for the binary schema parser
def test_parsing_invalid_binary_schema() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_rule('(R) ⫢ (φ ∧ )')

    assert str(excinfo.value) == 'Binary schemas must have a second sub-schema'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (R) ⫢ (φ ∧ )
          │       ^^^^^^
    ''')
