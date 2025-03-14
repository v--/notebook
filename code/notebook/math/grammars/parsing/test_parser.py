from textwrap import dedent

import pytest

from ....parsing import ParserError
from ....support.pytest import pytest_parametrize_kwargs, pytest_parametrize_lists
from ..alphabet import NonTerminal, Terminal
from ..grammar import GrammarRule, GrammarSchema
from .parser import parse_grammar_rule_line, parse_grammar_schema, parse_nonterminal, parse_terminal


@pytest_parametrize_lists(
    string=[
        '"T"',
        '"τ"',
        '"<"',
    ]
)
def test_parsing_valid_terminals(string: str) -> None:
    assert parse_terminal(string) == Terminal(string[1:-1])


def test_parsing_double_quote_terminal() -> None:
    assert parse_terminal('"\\""') == Terminal('"')


def test_parsing_terminal_empty_input() -> None:
    with pytest.raises(ParserError) as excinfo:
        assert parse_terminal('')

    assert str(excinfo.value) == 'Empty input'


def test_parsing_terminal_with_only_opening_quotes() -> None:
    with pytest.raises(ParserError) as excinfo:
        assert parse_terminal('"')

    assert str(excinfo.value) == 'Expected a terminal'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ "
          │ ^
        '''
    )


def test_parsing_empty_terminal() -> None:
    with pytest.raises(ParserError) as excinfo:
        assert parse_terminal('""')

    assert str(excinfo.value) == 'Empty terminals are disallowed'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ ""
          │ ^^
        '''
    )


def test_parsing_terminal_with_no_closing_quotes() -> None:
    with pytest.raises(ParserError) as excinfo:
        assert parse_terminal('"T')

    assert str(excinfo.value) == 'Terminal has no matching closing quotes'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ "T
          │ ^^
        '''
    )


def test_parsing_two_symbol_terminal() -> None:
    with pytest.raises(ParserError) as excinfo:
        assert parse_terminal('"TT"')

    assert str(excinfo.value) == 'Multi-symbol terminals are disallowed'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ "TT"
          │ ^^^^
        '''
    )


def test_parsing_two_symbol_non_text_terminal() -> None:
    with pytest.raises(ParserError) as excinfo:
        assert parse_terminal('"T<"')

    assert str(excinfo.value) == 'Multi-symbol terminals are disallowed'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ "T<"
          │ ^^^^
        '''
    )


@pytest_parametrize_lists(
    string=[
        '<N>',
        '<Text>',
        '<"Text">',
        '<Lorem ipsum>',
    ]
)
def test_parsing_valid_nonterminals(string: str) -> None:
    assert parse_nonterminal(string) == NonTerminal(string[1:-1])


def test_parsing_opening_chevron_nonterminal() -> None:
    assert parse_nonterminal('<\\<>') == NonTerminal('<')


def test_parsing_closing_chevron_nonterminal() -> None:
    assert parse_nonterminal('<\\>>') == NonTerminal('>')


def test_parsing_nonterminal_empty_input() -> None:
    with pytest.raises(ParserError) as excinfo:
        assert parse_nonterminal('')

    assert str(excinfo.value) == 'Empty input'


def test_parsing_nonterminal_with_only_opening_chevron() -> None:
    with pytest.raises(ParserError) as excinfo:
        assert parse_nonterminal('<')

    assert str(excinfo.value) == 'Expected a nonterminal'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ <
          │ ^
        '''
    )


def test_parsing_empty_nonterminal() -> None:
    with pytest.raises(ParserError) as excinfo:
        assert parse_nonterminal('<>')

    assert str(excinfo.value) == 'Empty nonterminals are disallowed'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ <>
          │ ^^
        '''
    )


def test_parsing_nonterminal_with_no_closing_chevron() -> None:
    with pytest.raises(ParserError) as excinfo:
        assert parse_nonterminal('<N')

    assert str(excinfo.value) == 'Nonterminal has no matching closing chevron'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ <N
          │ ^^
        '''
    )


def test_parsing_nested_nonterminal() -> None:
    with pytest.raises(ParserError) as excinfo:
        assert parse_nonterminal('<N<N>>')

    assert str(excinfo.value) == 'Nested nonterminals are disallowed'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ <N<N>>
          │ ^^^
        '''
    )


def test_parsing_empty_rule() -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_grammar_rule_line('')

    assert str(excinfo.value) == 'Expected a rule'


def test_parsing_rule_with_empty_left_side() -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_grammar_rule_line('→ ε')

    assert str(excinfo.value) == 'The left side of a rule must be nonempty'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ → ε
          │ ^
        '''
    )


def test_parsing_rule_with_lone_terminal_on_left() -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_grammar_schema('"a" → ε')

    assert str(excinfo.value) == 'The left side of a rule must contain at least one nonterminal'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ "a" → ε
          │ ^^^
        '''
    )


def test_parsing_rule_with_epsilon_on_left() -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_grammar_schema('ε → ε')

    assert str(excinfo.value) == 'ε is disallowed on the left side of a rule'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ ε → ε
          │ ^
        '''
    )


def test_parsing_rule_with_no_arrow() -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_grammar_schema('<S>')

    assert str(excinfo.value) == 'Expected an arrow after the left side of a rule'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ <S>
          │ ^^^
        '''
    )


def test_parsing_rule_with_empty_right_side() -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_grammar_schema('<S> →')

    assert str(excinfo.value) == 'The right side of a rule must contain a pipe between runs of terminals, nonterminals and ε'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ <S> →
          │ ^^^^^
        '''
    )


def test_parsing_rule_with_epsilon_and_nonterminal() -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_grammar_schema('<S> → ε <S>')

    assert str(excinfo.value) == 'The right side of a rule must contain terminals and nonterminals and at most a single ε'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ <S> → ε <S>
          │       ^^^^^
        '''
    )


def test_parsing_line_break_inside_rule() -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_grammar_schema(
            dedent('''\
                <S>
                → ε
                '''
            )
        )

    assert str(excinfo.value) == 'Expected an arrow after the left side of a rule'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ <S>↵
          │ ^^^
        '''
    )


def test_parsing_rule_with_two_right_sides() -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_grammar_schema(
            dedent('<S> → →')
        )

    assert str(excinfo.value) == 'The right side of a rule must contain terminals and nonterminals and at most a single ε'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ <S> → →
          │       ^
        '''
    )


def test_parsing_rule_with_two_nonempty_right_sides() -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_grammar_schema(
            dedent('<S> → "A" → "A"')
        )

    assert str(excinfo.value) == 'The right side of a rule must contain a pipe between runs of terminals, nonterminals and ε'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ <S> → "A" → "A"
          │       ^^^^^^^^^
        '''
    )


@pytest_parametrize_kwargs(
    dict(
        schema=dedent('''\
            <S> → <S>
            '''
        ),
        expected=GrammarSchema([
            GrammarRule([NonTerminal('S')], [NonTerminal('S')])
        ])
    ),

    dict(
        schema=dedent('''\
            <S> → ε | "a" <S>
            '''
        ),
        expected=GrammarSchema([
            GrammarRule([NonTerminal('S')], []),
            GrammarRule([NonTerminal('S')], [Terminal('a'), NonTerminal('S')]),
        ])
    ),

    dict(
        schema=dedent('''\
            <S> → ε
            <S> → "a" <S>
            '''
        ),
        expected=GrammarSchema([
            GrammarRule([NonTerminal('S')], []),
            GrammarRule([NonTerminal('S')], [Terminal('a'), NonTerminal('S')]),
        ])
    ),
)
def test_parse_schema_success(schema: str, expected: GrammarSchema) -> None:
    assert parse_grammar_schema(schema) == expected


def test_parsing_empty_schema() -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_grammar_schema('')

    assert str(excinfo.value) == 'Expected at least one grammar rule'
