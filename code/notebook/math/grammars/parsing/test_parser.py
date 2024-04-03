from textwrap import dedent

import pytest

from ....parsing.parser import ParsingError
from ..alphabet import NonTerminal, Terminal
from ..grammar import GrammarRule, GrammarSchema
from .parser import parse_grammar_schema


def test_valid_schemas() -> None:
    assert parse_grammar_schema(
        dedent('''\
            <S> → <S>
            '''
        )
    ) == GrammarSchema([
        GrammarRule([NonTerminal('S')], [NonTerminal('S')])
    ])

    assert parse_grammar_schema(
        dedent('''\
            <S> → ε | "a" <S>
            '''
        )
    ) == GrammarSchema([
        GrammarRule([NonTerminal('S')], []),
        GrammarRule([NonTerminal('S')], [Terminal('a'), NonTerminal('S')]),
    ])

    assert parse_grammar_schema(
        dedent('''\
            <S> → ε
            <S> → "a" <S>
            '''
        )
    ) == GrammarSchema([
        GrammarRule([NonTerminal('S')], []),
        GrammarRule([NonTerminal('S')], [Terminal('a'), NonTerminal('S')]),
    ])


def test_parsing_empty_schema() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_grammar_schema('')

    assert str(excinfo.value) == 'Expected at least one grammar rule'


def test_parsing_empty_left_side() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_grammar_schema('→ ε')

    assert str(excinfo.value) == 'The left side of a rule must be nonempty'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ → ε
          │ ^
        '''
    )


def test_parsing_lone_terminal_on_left() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_grammar_schema('"a" → ε')

    assert str(excinfo.value) == 'The left side of a rule must contain at least one nonterminal'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ "a" → ε
          │ ^^^
        '''
    )


def test_parsing_epsilon_on_left() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_grammar_schema('ε → ε')

    assert str(excinfo.value) == 'The left side of a rule must consist of only terminals and nonterminals'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ ε → ε
          │ ^
        '''
    )


def test_parsing_pipe_on_left() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_grammar_schema('<S> | <A> → ε')

    assert str(excinfo.value) == 'Expected an arrow after the rule source'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ <S> | <A> → ε
          │     ^
        '''
    )


def test_parsing_rule_with_epsilon_and_nonterminal() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_grammar_schema('<S> → ε <S>')

    assert str(excinfo.value) == 'ε is only allowed on its own on the right side of a rule'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ <S> → ε <S>
          │       ^
        '''
    )


def test_parsing_line_break_inside_rule() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_grammar_schema(
            dedent('''\
                <S>
                → ε
                '''
            )
        )

    assert str(excinfo.value) == 'Expected an arrow after the rule source'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ <S>↵
          │    ^
        '''
    )


def test_parsing_invalid_right_side() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_grammar_schema(
            dedent('<S> → →')
        )

    assert str(excinfo.value) == 'The right side of a rule must contain only terminals and nonterminals and at most a single ε'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ <S> → →
          │       ^
        '''
    )


    with pytest.raises(ParsingError) as excinfo:
        parse_grammar_schema(
            dedent('<S> → "A" →')
        )

    assert str(excinfo.value) == 'The right side of a rule must contain a pipe between runs of terminals, nonterminals and ε'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ <S> → "A" →
          │           ^
        '''
    )
