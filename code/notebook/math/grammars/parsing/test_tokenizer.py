from textwrap import dedent

import pytest

from ....parsing.parser import ParsingError
from ..alphabet import NonTerminal, Terminal
from ..grammar import GrammarRule, GrammarSchema
from .tokenizer import tokenize_bnf


def test_valid_terminals():
    assert tokenize_bnf('"S"') == [Terminal('S')]


def test_invalid_terminals():
    with pytest.raises(ParsingError) as excinfo:
        tokenize_bnf('""')

    assert str(excinfo.value) == 'Empty terminals are disallowed'

    with pytest.raises(ParsingError) as excinfo:
        tokenize_bnf('"S')

    assert str(excinfo.value) == 'Terminal has no matching end quote'

    with pytest.raises(ParsingError) as excinfo:
        tokenize_bnf('"SS"')

    assert str(excinfo.value) == 'Multi-symbol terminals are disallowed'


def test_valid_nonterminals():
    assert tokenize_bnf('<S>') == [NonTerminal('S')]
    assert tokenize_bnf('<SS>') == [NonTerminal('SS')]

    assert tokenize_bnf(r'<\>>') == [NonTerminal('>')]
    assert tokenize_bnf(r'<\<>') == [NonTerminal('<')]
    assert tokenize_bnf(r'<\\>') == [NonTerminal('\\')]


def test_invalid_nonterminals():
    with pytest.raises(ParsingError) as excinfo:
        tokenize_bnf('<>')

    assert str(excinfo.value) == 'Empty nonterminals are disallowed'

    with pytest.raises(ParsingError) as excinfo:
        tokenize_bnf('<S')

    assert str(excinfo.value) == 'Nonterminal has no matching end bracket'

    with pytest.raises(ParsingError) as excinfo:
        tokenize_bnf('<S<S>>')

    assert str(excinfo.value) == 'Nonterminal names cannot be nested'
    assert excinfo.value.__notes__[0] == dedent('''\
    1 │ <S<S>>
      │ ^^^
    ''')

    with pytest.raises(ParsingError) as excinfo:
        tokenize_bnf(r'<S\r>')

    assert str(excinfo.value) == 'Invalid escape code'
    assert excinfo.value.__notes__[0] == dedent('''\
    1 │ <S\\r>
      │   ^^
    ''')
