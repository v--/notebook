import pytest

from ...support.parsing.parser import ParserError
from .parser import parse_rule


def test_parsing_atomic_valid():
    def is_rule_rebuilt(string: str):
        assert str(parse_rule(string)) == string

    is_rule_rebuilt('(R) ⇛ Ψ')
    is_rule_rebuilt('(R) Φ ⇛ Ψ')
    is_rule_rebuilt('(R) Φ₁, Φ₂ ⇛ Ψ')


def test_parsing_atomic_invalid():
    # There must be a name
    with pytest.raises(ParserError):
        parse_rule('Φ ⇛ Ψ')

    # The name must not be empty
    with pytest.raises(ParserError):
        parse_rule('() Φ ⇛ Ψ')

    # The name parentheses must be closed
    with pytest.raises(ParserError):
        parse_rule('(R Φ ⇛ Ψ')

    # Premises must be separated by commas
    with pytest.raises(ParserError):
        parse_rule('(R) Φ₁ Φ₂ ⇛ Ψ')

    # There must be a conclusion
    with pytest.raises(ParserError):
        parse_rule('(R) ⇛')


def test_parsing_markers_valid():
    def is_rule_rebuilt(string: str):
        assert str(parse_rule(string)) == string

    is_rule_rebuilt('(R) [θ] Φ ⇛ Ψ')


def test_parsing_markers_invalid():
    # The discharge brackets must be closed
    with pytest.raises(ParserError):
        parse_rule('(R) [θ Φ ⇛ Ψ')

    # The conclusion cannot have a marker
    with pytest.raises(ParserError):
        parse_rule('(R) ⇛ [θ] Ψ')


def test_parsing_complex_placeholders():
    def is_rule_rebuilt(string: str):
        assert str(parse_rule(string)) == string

    is_rule_rebuilt('(R) ⇛ ⊥')
    is_rule_rebuilt('(R) ⇛ ¬Ψ')
    is_rule_rebuilt('(R) ⇛ (Ψ₁ ∧ Ψ₂)')
    is_rule_rebuilt('(R) ⇛ ∀ξ.Ψ')
