from textwrap import dedent
from typing import TYPE_CHECKING, NamedTuple

import pytest

from ...support.coderefs import collector
from .brute_force_parse import derives
from .parsing import parse_grammar_schema
from .symbols import NonTerminal


if TYPE_CHECKING:
    from collections.abc import Sequence

    from .grammar import Grammar


class GrammarFixture(NamedTuple):
    grammar: Grammar
    whitelist: Sequence[str]
    blacklist: Sequence[str]

    # ruff: disable[S101]
    def assert_equivalent(self, other: Grammar) -> None:
        for string in self.whitelist:
            assert derives(other, string)

        for string in self.blacklist:
            assert not derives(other, string)

    # ruff: enable[S101]


@pytest.fixture
@collector.ref('ex:def:chomsky_hierarchy/an')
def an() -> GrammarFixture:
    schema = parse_grammar_schema(
        dedent('''\
            <S> → ε
            <S> → <A>
            <A> → <A> "a"
            <A> → "a"
            ''',
        ),
    )

    return GrammarFixture(
        grammar=schema.instantiate(NonTerminal('S')),
        whitelist=['', 'a', 'aaa', 'aaaaaa'],
        blacklist=['b', 'ba', 'ab'],
    )


@pytest.fixture
@collector.ref('ex:def:chomsky_hierarchy/anbn')
def anbn() -> GrammarFixture:
    schema = parse_grammar_schema(
        dedent('''\
            <S> → ε
            <S> → <A>
            <A> → "a" <A> "b"
            <A> → "a" "b"
            ''',
        ),
    )

    return GrammarFixture(
        grammar=schema.instantiate(NonTerminal('S')),
        whitelist=['', 'ab', 'aaabbb'],
        blacklist=['a', 'ba'],
    )


@pytest.fixture
@collector.ref('ex:def:chomsky_hierarchy/anbncn')
def anbncn() -> GrammarFixture:
    schema = parse_grammar_schema(
        dedent('''\
            <S> → "a" "b" "c"
            <S> → "a" <S> <B> "c"
            <S> → ε
            "c" <B> → <B> "c"
            "b" <B> → "b" "b"
            ''',
        ),
    )

    return GrammarFixture(
        grammar=schema.instantiate(NonTerminal('S')),
        whitelist=['', 'abc', 'aabbcc'],
        blacklist=['abbcc', 'aabcc', 'aabbc'],
    )


@pytest.fixture
def s3() -> GrammarFixture:
    schema = parse_grammar_schema(
        dedent('''\
            <S> → ε
            <S> → <S> <S> <S>
            <S> → "a"
            ''',
        ),
    )

    return GrammarFixture(
        grammar=schema.instantiate(NonTerminal('S')),
        whitelist=['a', 'aa', 'aaa', 'aaaa'],
        blacklist=['b'],
    )


@pytest.fixture
def binary() -> GrammarFixture:
    schema = parse_grammar_schema(
        dedent('''\
            <N> → "0" | "1" | "1" <B>
            <B> → "0" | "0" <B> | "1" | "1" <B>
            ''',
        ),
    )

    return GrammarFixture(
        grammar=schema.instantiate(NonTerminal('N')),
        whitelist=['0', '1', '10', '11', '100', '101'],
        blacklist=['', '01'],
    )
