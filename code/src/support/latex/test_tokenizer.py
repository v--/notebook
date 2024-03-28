import pytest

from ..parsing.parser import ParserError

from .tokens import WordToken, EscapedWordToken, WhitespaceToken, SpecialToken
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
    assert tokenize_latex('\\test_test') == [EscapedWordToken('test'), SpecialToken.underscore_token, WordToken('test')]


def test_escaped_whitespace():
    string = '\\ '
    tokens = tokenize_latex(string)
    assert tokens == [EscapedWordToken(' ')]


def test_single_space():
    string = ' '
    tokens = tokenize_latex(string)
    assert tokens == [WhitespaceToken(' ')]


def test_multiple_spaces():
    string = '   '
    tokens = tokenize_latex(string)
    assert tokens == [WhitespaceToken('   ')]


def test_multiple_tabs():
    string = '\t' * 3
    tokens = tokenize_latex(string)
    assert tokens == [WhitespaceToken('\t' * 3)]


def test_multiple_newlines():
    string = '\n' * 3
    tokens = tokenize_latex(string)
    assert tokens == [WhitespaceToken('\n' * 3)]


def test_ampersand():
    string = '&'
    tokens = tokenize_latex(string)
    assert tokens == [SpecialToken.ampersand_token]


def test_caret():
    string = '^'
    tokens = tokenize_latex(string)
    assert tokens == [SpecialToken.caret_token]


def test_underscore():
    string = '_'
    tokens = tokenize_latex(string)
    assert tokens == [SpecialToken.underscore_token]


def test_command():
    string = '\\sum_{k \\in \\mscrK}'
    tokens = tokenize_latex(string)
    assert tokens == [EscapedWordToken('sum'), SpecialToken.underscore_token, SpecialToken.opening_brace, WordToken('k'), WhitespaceToken(' '), EscapedWordToken('in'), WhitespaceToken(' '), EscapedWordToken('mscrK'), SpecialToken.closing_brace]


def test_real():
    with open('../figures/thm__natural_number_divisibility_order.tex') as file:
        string = file.read()
        tokens = tokenize_latex(string)
        assert ''.join(str(t) for t in tokens) == string
