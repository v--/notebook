import pytest

from .grammar import GrammarSchema, NonTerminal


@pytest.fixture
def an():
    schema = GrammarSchema.parse('''
        <S> → ε
        <S> → <A>
        <A> → <A> "a"
        <A> → "a"
    ''')
    return schema.instantiate(NonTerminal('S'))


@pytest.fixture
def anbn():
    schema = GrammarSchema.parse('''
        <S> → ε
        <S> → <A>
        <A> → "a" <A> "b"
        <A> → "a" "b"
    ''')

    return schema.instantiate(NonTerminal('S'))


@pytest.fixture
def s3():
    schema = GrammarSchema.parse('''
        <S> → ε
        <S> → <S> <S> <S>
        <S> → "a"
    ''')

    return schema.instantiate(NonTerminal('S'))
