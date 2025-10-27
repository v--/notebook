from collections.abc import Sequence
from textwrap import dedent
from typing import NamedTuple

import pytest

from .alphabet import NonTerminal
from .brute_force_parse import derives
from .grammar import Grammar
from .parsing import parse_grammar_schema


class GrammarFixture(NamedTuple):
    grammar: Grammar
    whitelist: Sequence[str]
    blacklist: Sequence[str]

    def assert_equivalent(self, other: Grammar) -> None:
        for string in self.whitelist:
            assert derives(other, string)

        for string in self.blacklist:
            assert not derives(other, string)


@pytest.fixture
def an() -> GrammarFixture:
    schema = parse_grammar_schema(
        dedent('''\
            <S> → ε
            <S> → <A>
            <A> → <A> "a"
            <A> → "a"
            '''
        )
    )

    return GrammarFixture(
        grammar=schema.instantiate(NonTerminal('S')),
        whitelist=['', 'a', 'aaa', 'aaaaaa'],
        blacklist=['b', 'ba', 'ab']
    )


@pytest.fixture
def anbn() -> GrammarFixture:
    schema = parse_grammar_schema(
        dedent('''\
            <S> → ε
            <S> → <A>
            <A> → "a" <A> "b"
            <A> → "a" "b"
            '''
        )
    )

    return GrammarFixture(
        grammar=schema.instantiate(NonTerminal('S')),
        whitelist=['', 'ab', 'aaabbb'],
        blacklist=['a', 'ba']
    )


@pytest.fixture
def s3() -> GrammarFixture:
    schema = parse_grammar_schema(
        dedent('''\
            <S> → ε
            <S> → <S> <S> <S>
            <S> → "a"
            '''
        )
    )

    return GrammarFixture(
        grammar=schema.instantiate(NonTerminal('S')),
        whitelist=['a', 'aa', 'aaa', 'aaaa'],
        blacklist=['b']
    )


@pytest.fixture
def binary() -> GrammarFixture:
    schema = parse_grammar_schema(
        dedent('''\
            <N> → "0" | "1" | "1" <B>
            <B> → "0" | "0" <B> | "1" | "1" <B>
            '''
        )
    )

    return GrammarFixture(
        grammar=schema.instantiate(NonTerminal('N')),
        whitelist=['0', '1', '10', '11', '100', '101'],
        blacklist=['', '01']
    )
