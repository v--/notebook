from textwrap import dedent

import pytest

from ....parsing.parser import ParsingError
from .parser import parse_rule


def test_parsing_atomic_valid() -> None:
    def assert_rule_rebuilt(string: str) -> None:
        assert str(parse_rule(string)) == string

    assert_rule_rebuilt('(R) ⫢ Ψ')
    assert_rule_rebuilt('(R) Φ ⫢ Ψ')
    assert_rule_rebuilt('(R) Φ₁, Φ₂ ⫢ Ψ')


def test_parsing_without_rule_name() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_rule('Φ ⫢ Ψ')

    assert str(excinfo.value) == 'A rule must start with a parenthesized name'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ Φ ⫢ Ψ
          │ ^
        '''
    )


def test_parsing_with_empty_name() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_rule('() Φ ⫢ Ψ')

    assert str(excinfo.value) == 'The name of a rule must be a Latin identifier'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ () Φ ⫢ Ψ
          │ ^^
        '''
    )


def test_parsing_rule_with_unclosed_parens() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_rule('(R Φ ⫢ Ψ')

    assert str(excinfo.value) == 'Unclosed parenthesis after rule name'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (R Φ ⫢ Ψ
          │ ^^^
        '''
    )


def test_parsing_rule_with_no_comma() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_rule('(R) Φ₁ Φ₂ ⫢ Ψ')

    assert str(excinfo.value) == 'Expected either a comma or a sequent symbol after a placeholder'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (R) Φ₁ Φ₂ ⫢ Ψ
          │        ^^
        '''
    )


def test_parsing_rule_with_no_conclusion() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_rule('(R) Φ')

    assert str(excinfo.value) == 'Expected a sequent symbol'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (R) Φ
          │     ^
        '''
    )


def test_parsing_valid_discharge_placeholders() -> None:
    def assert_rule_rebuilt(string: str) -> None:
        assert str(parse_rule(string)) == string

    assert_rule_rebuilt('(R) [θ] Φ ⫢ Ψ')


def test_parsing_discharge_placeholder_with_no_name() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_rule('(R) [] Φ ⫢ Ψ')

    assert str(excinfo.value) == 'Unexpected token'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (R) [] Φ ⫢ Ψ
          │      ^
        '''
    )


def test_parsing_discharge_placeholder_with_no_closing_bracket() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_rule('(R) [θ Φ ⫢ Ψ')

    assert str(excinfo.value) == 'Unclosed brackets for discharge placeholders'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (R) [θ Φ ⫢ Ψ
          │     ^^^
        '''
    )


def test_parsing_discharge_in_conclusion() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_rule('(R) ⫢ [Θ] Ψ')

    assert str(excinfo.value) == 'The conclusion cannot have a discharge placeholder'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (R) ⫢ [Θ] Ψ
          │       ^^^^^
        '''
    )


def test_parsing_complex_placeholders() -> None:
    def assert_rule_rebuilt(string: str) -> None:
        assert str(parse_rule(string)) == string

    assert_rule_rebuilt('(R) ⫢ ⊥')
    assert_rule_rebuilt('(R) ⫢ ¬Ψ')
    assert_rule_rebuilt('(R) ⫢ (Ψ₁ ∧ Ψ₂)')
    assert_rule_rebuilt('(R) ⫢ ∀ξ.Ψ')


# The quantifier parser is an almost literal copy of the one from the FOL parser, so we rely on the tests there
def test_parsing_quantifier_placeholder_with_no_dot() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_rule('(R) ⫢ ∀ξΨ')

    assert str(excinfo.value) == 'Expected dot after variable'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (R) ⫢ ∀ξΨ
          │       ^^^
    ''')


# The same goes for the binary placeholder parser
def test_parsing_invalid_binary_placeholder() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_rule('(R) ⫢ (Φ ∧ )')

    assert str(excinfo.value) == 'Binary placeholders must have a second sub-placeholder'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (R) ⫢ (Φ ∧ )
          │       ^^^^^^
    ''')
