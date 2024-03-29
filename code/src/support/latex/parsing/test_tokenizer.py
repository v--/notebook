import pytest

from ...parsing.parser import ParserError

from .tokens import WordToken, EscapedWordToken, MiscToken
from .tokenizer import tokenize_latex


def test_empty_string():
    string = ''
    tokens = tokenize_latex(string)
    assert tokens == []


def test_latin_word():
    string = 'test'
    tokens = tokenize_latex(string)
    assert tokens == [WordToken('test')]


def test_cyrillic_word():
    string = 'тест'
    tokens = tokenize_latex(string)
    assert tokens == [WordToken('тест')]


def test_numeric_word():
    string = '1153'
    tokens = tokenize_latex(string)
    assert tokens == [WordToken('1153')]


def test_empty_escaped():
    with pytest.raises(ParserError):
        tokenize_latex('\\')


def test_latin_escaped():
    assert tokenize_latex('\\test') == [EscapedWordToken('test')]


def test_escaped_with_underscore():
    assert tokenize_latex('\\test_test') == [EscapedWordToken('test'), MiscToken.underscore, WordToken('test')]


def test_escaped_whitespace():
    string = '\\ '
    tokens = tokenize_latex(string)
    assert tokens == [EscapedWordToken(' ')]


def test_single_space():
    string = ' '
    tokens = tokenize_latex(string)
    assert tokens == [MiscToken.space]


def test_multiple_spaces():
    string = ' ' * 3
    tokens = tokenize_latex(string)
    assert tokens == [MiscToken.space] * 3


def test_multiple_tabs():
    string = '\t' * 3
    tokens = tokenize_latex(string)
    assert tokens == [MiscToken.tab] * 3


def test_multiple_line_breaks():
    string = '\n' * 3
    tokens = tokenize_latex(string)
    assert tokens == [MiscToken.line_break] * 3


def test_ampersand():
    string = '&'
    tokens = tokenize_latex(string)
    assert tokens == [MiscToken.ampersand]


def test_caret():
    string = '^'
    tokens = tokenize_latex(string)
    assert tokens == [MiscToken.caret]


def test_underscore():
    string = '_'
    tokens = tokenize_latex(string)
    assert tokens == [MiscToken.underscore]


def test_command():
    string = '\\sum_{k \\in \\mscrK}'
    tokens = tokenize_latex(string)
    assert tokens == [EscapedWordToken('sum'), MiscToken.underscore, MiscToken.opening_brace, WordToken('k'), MiscToken.space, EscapedWordToken('in'), MiscToken.space, EscapedWordToken('mscrK'), MiscToken.closing_brace]


def test_real():
    with open('../figures/thm__natural_number_divisibility_order.tex') as file:
        string = file.read()
        tokens = tokenize_latex(string)
        assert ''.join(str(t) for t in tokens) == string
