from typing import TYPE_CHECKING

from ...support.pytest import pytest_parametrize_lists
from .context_sensitive import (
    is_context_sensitive_grammar,
    is_context_sensitive_rule,
    length_increasing_to_context_sensitive,
)
from .parsing import parse_grammar_schema


if TYPE_CHECKING:
    from .conftest import GrammarFixture


@pytest_parametrize_lists(
    rule=[
        '<S> → <S>',
        '<S> → "a"',
        '<S> → "a" "b" "c"',
        '"a" <B> "c" → "a" "b" "c"',
        '"a" <BC> "d" → "a" "b" "c" "d"',
    ],
)
def test_is_context_sensitive_rule_success(rule: str) -> None:
    rule_ = parse_grammar_schema(rule).rules[0]
    assert is_context_sensitive_rule(rule_)


@pytest_parametrize_lists(
    rule=[
        '<S> → ε',
        '"a" <B> "c" → "a" "c"',
        '"a" <BC> "d" → "b" "c"',
    ],
)
def test_is_context_sensitive_rule_failure(rule: str) -> None:
    rule_ = parse_grammar_schema(rule).rules[0]
    assert not is_context_sensitive_rule(rule_)


def test_is_context_sensitive_grammar_anbncn(anbncn: GrammarFixture) -> None:
    assert not is_context_sensitive_grammar(anbncn.grammar)


def test_length_increasing_to_context_sensitive_anbncn(anbncn: GrammarFixture) -> None:
    transformed = length_increasing_to_context_sensitive(anbncn.grammar)
    assert is_context_sensitive_grammar(transformed)
