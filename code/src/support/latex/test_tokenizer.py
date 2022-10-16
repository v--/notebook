import pytest

from ..parsing import ParserError

from .tokens import LaTeXToken, Word, EscapedWord, ampersand, underscore, caret, opening_brace, closing_brace, Whitespace, single_space, tab, newline
from .tokenizer import tokenize_latex


def test_empty_string():
    string = ''
    tokens = tokenize_latex(string)
    assert tokens == []


def test_latin_word():
    string = 'test'
    tokens = tokenize_latex(string)
    assert tokens == [Word('test')]


def test_cyrillic_word():
    string = 'тест'
    tokens = tokenize_latex(string)
    assert tokens == [Word('тест')]


def test_numeric_word():
    string = '1153'
    tokens = tokenize_latex(string)
    assert tokens == [Word('1153')]


def test_empty_escaped():
    with pytest.raises(ParserError):
        tokenize_latex('\\')


def test_escaped_whitespace():
    string = '\\ '
    tokens = tokenize_latex(string)
    assert tokens == [EscapedWord(' ')]


def test_single_space():
    string = ' '
    tokens = tokenize_latex(string)
    assert tokens == [single_space]


def test_multiple_spaces():
    string = '   '
    tokens = tokenize_latex(string)
    assert tokens == [Whitespace('   ')]


def test_single_tab():
    string = '\t'
    tokens = tokenize_latex(string)
    assert tokens == [tab]


def test_multiple_tabs():
    string = '\t' * 3
    tokens = tokenize_latex(string)
    assert tokens == [Whitespace('\t' * 3)]


def test_single_newine():
    string = '\n'
    tokens = tokenize_latex(string)
    assert tokens == [newline]


def test_multiple_newlines():
    string = '\n' * 3
    tokens = tokenize_latex(string)
    assert tokens == [Whitespace('\n' * 3)]


def test_ampersand():
    string = '&'
    tokens = tokenize_latex(string)
    assert tokens == [ampersand]


def test_caret():
    string = '^'
    tokens = tokenize_latex(string)
    assert tokens == [caret]


def test_underscore():
    string = '_'
    tokens = tokenize_latex(string)
    assert tokens == [underscore]


def test_command():
    string = '\\sum_{k \\in \\mscrK}'
    tokens = tokenize_latex(string)
    assert tokens == [EscapedWord('sum'), underscore, opening_brace, Word('k'), single_space, EscapedWord('in'), single_space, EscapedWord('mscrK'), closing_brace]


def test_real():
    with open('../figures/thm__natural_number_divisibility_order.tex') as file:
        string = file.read()
        tokens = tokenize_latex(string)
        assert ''.join(str(t) for t in tokens) == string
