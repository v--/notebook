from textwrap import dedent
from typing import TYPE_CHECKING

from ...support.pytest import pytest_parametrize_lists
from .context_sensitive import is_essentially_length_increasing_grammar, is_length_increasing_grammar, naive_membership
from .parsing import parse_grammar_schema
from .symbols import NonTerminal


if TYPE_CHECKING:
    from .conftest import GrammarFixture


def test_is_length_increasing_grammar_an(an: GrammarFixture) -> None:
    assert not is_length_increasing_grammar(an.grammar)
    assert is_essentially_length_increasing_grammar(an.grammar)


def test_is_length_increasing_grammar_binary(binary: GrammarFixture) -> None:
    assert is_length_increasing_grammar(binary.grammar)


def test_is_length_increasing_grammar_anbncn(anbncn: GrammarFixture) -> None:
    assert is_essentially_length_increasing_grammar(anbncn.grammar)


def test_is_length_increasing_grammar_failure() -> None:
    schema = parse_grammar_schema(
        dedent('''\
            <S> → "a" <S> "b"
            "a" <S> "b" → <S>
            ''',
        ),
    )

    grammar = schema.instantiate(NonTerminal('S'))
    assert not is_essentially_length_increasing_grammar(grammar)


def test_naive_membership_an(an: GrammarFixture) -> None:
    for string in an.whitelist:
        assert naive_membership(an.grammar, string)

    for string in an.blacklist:
        assert not naive_membership(an.grammar, string)


def test_naive_membership_anbn(anbn: GrammarFixture) -> None:
    for string in anbn.whitelist:
        assert naive_membership(anbn.grammar, string)

    for string in anbn.blacklist:
        assert not naive_membership(anbn.grammar, string)
