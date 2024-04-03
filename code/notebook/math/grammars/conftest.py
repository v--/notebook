from textwrap import dedent

import pytest

from .alphabet import NonTerminal
from .brute_force_parse import derives
from .grammar import Grammar
from .parsing.parser import parse_grammar_schema


@pytest.fixture()
def an() -> Grammar:
    schema = parse_grammar_schema(
        dedent('''\
            <S> → ε
            <S> → <A>
            <A> → <A> "a"
            <A> → "a"
            '''
        )
    )

    return schema.instantiate(NonTerminal('S'))


def assert_an(an: Grammar) -> None:
    assert derives(an, '')
    assert derives(an, 'a')
    assert derives(an, 'aaa')
    assert derives(an, 'aaaaaa')

    assert not derives(an, 'b')
    assert not derives(an, 'ba')
    assert not derives(an, 'ab')


@pytest.fixture()
def anbn() -> Grammar:
    schema = parse_grammar_schema(
        dedent('''\
            <S> → ε
            <S> → <A>
            <A> → "a" <A> "b"
            <A> → "a" "b"
            '''
        )
    )

    return schema.instantiate(NonTerminal('S'))


def assert_anbn(anbn: Grammar) -> None:
    assert derives(anbn, '')
    assert derives(anbn, 'ab')
    assert derives(anbn, 'aaabbb')

    assert not derives(anbn, 'a')
    assert not derives(anbn, 'ba')


@pytest.fixture()
def s3() -> Grammar:
    schema = parse_grammar_schema(
        dedent('''\
            <S> → ε
            <S> → <S> <S> <S>
            <S> → "a"
            '''
        )
    )

    return schema.instantiate(NonTerminal('S'))


def assert_s3(s3: Grammar) -> None:
    assert derives(s3, '')
    assert derives(s3, 'a')
    assert derives(s3, 'aa')
    assert derives(s3, 'aaa')
    assert derives(s3, 'aaaa')

    assert not derives(s3, 'b')


@pytest.fixture()
def binary() -> Grammar:
    schema = parse_grammar_schema(
        dedent('''\
            <N> → "0" | "1" | "1" <B>
            <B> → "0" | "0" <B> | "1" | "1" <B>
            '''
        )
    )

    return schema.instantiate(NonTerminal('N'))


def assert_binary(binary: Grammar) -> None:
    assert derives(binary, '0')
    assert derives(binary, '1')
    assert derives(binary, '10')
    assert derives(binary, '11')
    assert derives(binary, '100')
    assert derives(binary, '101')

    assert not derives(binary, '')
    assert not derives(binary, '01')
