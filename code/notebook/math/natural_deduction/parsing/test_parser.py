from textwrap import dedent

import pytest

from ....parsing.parser import ParsingError
from .parser import parse_rule


def test_parsing_atomic_valid() -> None:
    def assert_rule_rebuilt(string: str) -> None:
        assert str(parse_rule(string)) == string

    assert_rule_rebuilt('(R) ⫢ ψ')
    assert_rule_rebuilt('(R) φ ⫢ ψ')
    assert_rule_rebuilt('(R) φ₁, φ₂ ⫢ ψ')


def xtest_parsing_without_rule_name() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_rule('φ ⫢ ψ')

    assert str(excinfo.value) == 'A rule must start with a parenthesized name'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ φ ⫢ ψ
          │ ^
        '''
    )


def xtest_parsing_with_empty_name() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_rule('() φ ⫢ ψ')

    assert str(excinfo.value) == 'The name of a rule cannot be empty'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ () φ ⫢ ψ
          │ ^^
        '''
    )


def xtest_parsing_rule_with_unclosed_parens() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_rule('(R Φ ⫢ Ψ')

    assert str(excinfo.value) == 'Unclosed parenthesis after rule name'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (R Φ ⫢ Ψ
          │ ^^^
        '''
    )


def xtest_parsing_rule_with_no_comma() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_rule('(R) Φ₁ Φ₂ ⫢ Ψ')

    assert str(excinfo.value) == 'Expected either a comma or a sequent symbol after a schema'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (R) Φ₁ Φ₂ ⫢ Ψ
          │        ^^
        '''
    )


def xtest_parsing_rule_with_no_conclusion() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_rule('(R) Φ')

    assert str(excinfo.value) == 'Expected a sequent symbol'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (R) Φ
          │     ^
        '''
    )


def xtest_parsing_valid_discharge_schemas() -> None:
    def assert_rule_rebuilt(string: str) -> None:
        assert str(parse_rule(string)) == string

    assert_rule_rebuilt('(R) [θ] Φ ⫢ Ψ')


def xtest_parsing_discharge_schema_with_no_name() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_rule('(R) [] Φ ⫢ Ψ')

    assert str(excinfo.value) == 'Unexpected token'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (R) [] Φ ⫢ Ψ
          │      ^
        '''
    )


def xtest_parsing_discharge_schema_with_no_closing_bracket() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_rule('(R) [θ Φ ⫢ Ψ')

    assert str(excinfo.value) == 'Unclosed brackets for discharge schemas'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (R) [θ Φ ⫢ Ψ
          │     ^^^
        '''
    )


def xtest_parsing_discharge_in_conclusion() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_rule('(R) ⫢ [Θ] Ψ')

    assert str(excinfo.value) == 'The conclusion cannot have a discharge schema'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (R) ⫢ [Θ] Ψ
          │       ^^^^^
        '''
    )


def xtest_parsing_complex_schemas() -> None:
    def assert_rule_rebuilt(string: str) -> None:
        assert str(parse_rule(string)) == string

    assert_rule_rebuilt('(R) ⫢ ⊥')
    assert_rule_rebuilt('(R) ⫢ ¬Ψ')
    assert_rule_rebuilt('(R) ⫢ (Ψ₁ ∧ Ψ₂)')
    assert_rule_rebuilt('(R) ⫢ ∀ξ.Ψ')


# The quantifier parser is an almost literal copy of the one from the FOL parser, so we rely on the tests there
def xtest_parsing_quantifier_schema_with_no_dot() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_rule('(R) ⫢ ∀ξΨ')

    assert str(excinfo.value) == 'Expected dot after variable'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (R) ⫢ ∀ξΨ
          │       ^^^
    ''')


# The same goes for the binary schema parser
def xtest_parsing_invalid_binary_schema() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_rule('(R) ⫢ (Φ ∧ )')

    assert str(excinfo.value) == 'Binary schemas must have a second sub-schema'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (R) ⫢ (Φ ∧ )
          │       ^^^^^^
    ''')
