from textwrap import dedent

import pytest

from ....parsing.parser import ParsingError
from ..alphabet import NonTerminal, Terminal
from .tokenizer import tokenize_bnf


def test_parsing_valid_terminals():
    assert tokenize_bnf('"S"') == [Terminal('S')]


def test_parsing_empty_terminal():
    with pytest.raises(ParsingError) as excinfo:
        tokenize_bnf('""')

    assert str(excinfo.value) == 'Empty terminals are disallowed'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ ""
          │ ^^
        '''
    )


def test_parsing_invalid_incomplete_terminals():
    with pytest.raises(ParsingError) as excinfo:
        tokenize_bnf('"S')

    assert str(excinfo.value) == 'Terminal has no matching end quote'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ "S
          │ ^^
        '''
    )


def test_parsing_multichar_terminals():
    with pytest.raises(ParsingError) as excinfo:
        tokenize_bnf('"SS"')

    assert str(excinfo.value) == 'Multi-symbol terminals are disallowed'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ "SS"
          │ ^^^
        '''
    )


def test_parsing_valid_nonterminals():
    assert tokenize_bnf('<S>') == [NonTerminal('S')]
    assert tokenize_bnf('<SS>') == [NonTerminal('SS')]

    assert tokenize_bnf(r'<\>>') == [NonTerminal('>')]
    assert tokenize_bnf(r'<\<>') == [NonTerminal('<')]
    assert tokenize_bnf(r'<\\>') == [NonTerminal('\\')]


def test_parsing_invalid_nonterminals():
    with pytest.raises(ParsingError) as excinfo:
        tokenize_bnf('<>')

    assert str(excinfo.value) == 'Empty nonterminals are disallowed'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ <>
          │ ^^
        '''
    )


def test_parsing_unclosed_nonterminal_brace():
    with pytest.raises(ParsingError) as excinfo:
        tokenize_bnf('<S')

    assert str(excinfo.value) == 'Nonterminal has no matching end bracket'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ <S
          │ ^^
        '''
    )


def test_parsing_nested_nonterminals():
    with pytest.raises(ParsingError) as excinfo:
        tokenize_bnf('<S<S>>')

    assert str(excinfo.value) == 'Nonterminal names cannot be nested'
    assert excinfo.value.__notes__[0] == dedent('''\
    1 │ <S<S>>
      │ ^^^
    ''')


def test_parsing_invalid_escape_code():
    with pytest.raises(ParsingError) as excinfo:
        tokenize_bnf(r'<S\r>')

    assert str(excinfo.value) == 'Invalid escape code'
    assert excinfo.value.__notes__[0] == dedent('''\
    1 │ <S\\r>
      │   ^^
    ''')
