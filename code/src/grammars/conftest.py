import pytest

from .grammar import Grammar, GrammarSchema, NonTerminal
from .brute_force_parse import derives


@pytest.fixture
def an():
    schema = GrammarSchema.parse('''
        <S> → ε
        <S> → <A>
        <A> → <A> "a"
        <A> → "a"
    ''')
    return schema.instantiate(NonTerminal('S'))


def assert_an(an: Grammar):
    assert derives(an, '')
    assert derives(an, 'a')
    assert derives(an, 'aaa')
    assert derives(an, 'aaaaaa')

    assert not derives(an, 'b')
    assert not derives(an, 'ba')
    assert not derives(an, 'ab')


@pytest.fixture
def anbn():
    schema = GrammarSchema.parse('''
        <S> → ε
        <S> → <A>
        <A> → "a" <A> "b"
        <A> → "a" "b"
    ''')

    return schema.instantiate(NonTerminal('S'))


def assert_anbn(anbn: Grammar):
    assert derives(anbn, '')
    assert derives(anbn, 'ab')
    assert derives(anbn, 'aaabbb')

    assert not derives(anbn, 'a')
    assert not derives(anbn, 'ba')


@pytest.fixture
def s3():
    schema = GrammarSchema.parse('''
        <S> → ε
        <S> → <S> <S> <S>
        <S> → "a"
    ''')

    return schema.instantiate(NonTerminal('S'))


def assert_s3(s3: Grammar):
    assert derives(s3, '')
    assert derives(s3, 'a')
    assert derives(s3, 'aa')
    assert derives(s3, 'aaa')
    assert derives(s3, 'aaaa')

    assert not derives(s3, 'b')


@pytest.fixture
def binary():
    schema = GrammarSchema.parse('''
        <N> → "0" | "1" | "1" <B>
        <B> → "0" | "0" <B> | "1" | "1" <B>
    ''')

    return schema.instantiate(NonTerminal('N'))


def assert_binary(binary: Grammar):
    assert derives(binary, '0')
    assert derives(binary, '1')
    assert derives(binary, '10')
    assert derives(binary, '11')
    assert derives(binary, '100')
    assert derives(binary, '101')

    assert not derives(binary, '')
    assert not derives(binary, '01')
