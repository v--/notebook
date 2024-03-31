import pytest

from ....parsing.parser import ParsingError
from ..alphabet import NonTerminal, Terminal
from ..grammar import GrammarRule, GrammarSchema
from .parser import parse_grammar_schema


def test_valid_schemas():
    assert parse_grammar_schema('''
        <S> → <S>
    ''') == GrammarSchema([
        GrammarRule([NonTerminal('S')], [NonTerminal('S')])
    ])

    assert parse_grammar_schema('''
        <S> → ε | "a" <S>
    ''') == GrammarSchema([
        GrammarRule([NonTerminal('S')], []),
        GrammarRule([NonTerminal('S')], [Terminal('a'), NonTerminal('S')]),
    ])

    assert parse_grammar_schema('''
        <S> → ε
        <S> → "a" <S>
    ''') == GrammarSchema([
        GrammarRule([NonTerminal('S')], []),
        GrammarRule([NonTerminal('S')], [Terminal('a'), NonTerminal('S')]),
    ])


def test_parsing_variables_invalid():
    # The schema must be nonempty
    with pytest.raises(ParsingError):
        parse_grammar_schema('')

    # The left side must have a nonterminal
    with pytest.raises(ParsingError):
        parse_grammar_schema('"a" → ε')

    # The left side must not contain ε
    with pytest.raises(ParsingError):
        parse_grammar_schema('ε → ε')

    # The right side must not contain anything after ε
    with pytest.raises(ParsingError):
        parse_grammar_schema('<S> → ε <S>')

    # No line break is allowed before the arrow
    with pytest.raises(ParsingError):
        parse_grammar_schema('''
            <S>
            → ε
        ''')

    # No line break is allowed after the arrow
    with pytest.raises(ParsingError):
        parse_grammar_schema('''
            <S> →
            ε
        ''')
