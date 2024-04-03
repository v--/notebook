from textwrap import dedent

import pytest

from ...parsing.parser import ParsingError
from ...parsing.whitespace import Whitespace
from .tokenizer import tokenize_latex
from .tokens import EscapedWordToken, MiscToken, WordToken


def test_empty_string() -> None:
    string = ''
    tokens = tokenize_latex(string)
    assert tokens == []


def test_latin_string() -> None:
    string = 'test'
    tokens = tokenize_latex(string)
    assert tokens == [WordToken('test')]


def test_cyrillic_string() -> None:
    string = 'тест'
    tokens = tokenize_latex(string)
    assert tokens == [WordToken('тест')]


def test_numeric_string() -> None:
    string = '1153'
    tokens = tokenize_latex(string)
    assert tokens == [WordToken('1153')]


def test_empty_escaped() -> None:
    with pytest.raises(ParsingError) as excinfo:
        tokenize_latex('\\')

    assert str(excinfo.value) == 'Unexpected end of input'
    assert excinfo.value.__notes__[0] == dedent(r'''
        1 │ \
          │ ^
        '''[1:]
    )


def test_invalid_escaped() -> None:
    with pytest.raises(ParsingError) as excinfo:
        tokenize_latex('\\3')

    assert str(excinfo.value) == 'Unrecognized escape character'
    assert excinfo.value.__notes__[0] == dedent(r'''
        1 │ \3
          │ ^^
        '''[1:]
    )


def test_latin_escaped() -> None:
    assert tokenize_latex('\\test') == [EscapedWordToken('test')]


def test_escaped_with_underscore() -> None:
    assert tokenize_latex('\\test_test') == [EscapedWordToken('test'), MiscToken.underscore, WordToken('test')]


def test_escaped_whitespace() -> None:
    string = '\\ '
    tokens = tokenize_latex(string)
    assert tokens == [EscapedWordToken(' ')]


def test_single_space() -> None:
    string = ' '
    tokens = tokenize_latex(string)
    assert tokens == [Whitespace.space]


def test_multiple_spaces() -> None:
    string = ' ' * 3
    tokens = tokenize_latex(string)
    assert tokens == [Whitespace.space] * 3


def test_tab() -> None:
    string = '\t'
    tokens = tokenize_latex(string)
    assert tokens == [Whitespace.tab]


def test_line_break() -> None:
    string = '\n'
    tokens = tokenize_latex(string)
    assert tokens == [Whitespace.line_break]


def test_ampersand() -> None:
    string = '&'
    tokens = tokenize_latex(string)
    assert tokens == [MiscToken.ampersand]


def test_caret() -> None:
    string = '^'
    tokens = tokenize_latex(string)
    assert tokens == [MiscToken.caret]


def test_underscore() -> None:
    string = '_'
    tokens = tokenize_latex(string)
    assert tokens == [MiscToken.underscore]


def test_command() -> None:
    string = '\\sum_{k \\in \\mscrK}'
    tokens = tokenize_latex(string)
    assert tokens == [
        EscapedWordToken('sum'),
        MiscToken.underscore,
        MiscToken.opening_brace,
        WordToken('k'),
        Whitespace.space,
        EscapedWordToken('in'),
        Whitespace.space,
        EscapedWordToken('mscrK'),
        MiscToken.closing_brace
    ]


def test_real() -> None:
    with open('../figures/thm__natural_number_divisibility_order.tex') as file:  # noqa: PTH123
        string = file.read()
        tokens = tokenize_latex(string)
        assert ''.join(str(t) for t in tokens) == string
