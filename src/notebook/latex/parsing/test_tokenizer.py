from ...paths import FIGURES_PATH
from .tokenizer import tokenize_latex
from .tokens import LaTeXToken


def test_empty_string() -> None:
    string = ''
    tokens = tokenize_latex(string)
    assert tokens == []


def test_latin_string() -> None:
    string = 'test'
    tokens = tokenize_latex(string)
    assert tokens == [
        LaTeXToken('TEXT', 'test', 0)
    ]


def test_cyrillic_string() -> None:
    string = 'тест'
    tokens = tokenize_latex(string)
    assert tokens == [
        LaTeXToken('TEXT', 'тест', 0)
    ]


def test_numeric_string() -> None:
    string = '1153'
    tokens = tokenize_latex(string)
    assert tokens == [
        LaTeXToken('TEXT', '1153', 0)
    ]


def test_latin_escaped() -> None:
    string = '\\test'
    tokens = tokenize_latex(string)
    assert tokens == [
        LaTeXToken('BACKSLASH', '\\', 0),
        LaTeXToken('TEXT', 'test', 1)
    ]


def test_escaped_with_underscore() -> None:
    string = '\\test_test'
    tokens = tokenize_latex(string)
    assert tokens == [
        LaTeXToken('BACKSLASH', '\\', 0),
        LaTeXToken('TEXT', 'test', 1),
        LaTeXToken('UNDERSCORE', '_', 5),
        LaTeXToken('TEXT', 'test', 6)
    ]


def test_escaped_whitespace() -> None:
    string = '\\ '
    tokens = tokenize_latex(string)
    assert tokens == [
        LaTeXToken('BACKSLASH', '\\', 0),
        LaTeXToken('WHITESPACE', ' ', 1)
    ]


def test_single_space() -> None:
    string = ' '
    tokens = tokenize_latex(string)
    assert tokens == [
        LaTeXToken('WHITESPACE', ' ', 0)
    ]


def test_multiple_spaces() -> None:
    string = '   '
    tokens = tokenize_latex(string)
    assert tokens == [
        LaTeXToken('WHITESPACE', '   ', 0)
    ]


def test_tab() -> None:
    string = '\t'
    tokens = tokenize_latex(string)
    assert tokens == [
        LaTeXToken('WHITESPACE', '\t', 0)
    ]


def test_line_break() -> None:
    string = '\n'
    tokens = tokenize_latex(string)
    assert tokens == [
        LaTeXToken('LINE_BREAK', '\n', 0)
    ]


def test_ampersand() -> None:
    string = '&'
    tokens = tokenize_latex(string)
    assert tokens == [
        LaTeXToken('AMPERSAND', '&', 0)
    ]


def test_caret() -> None:
    string = '^'
    tokens = tokenize_latex(string)
    assert tokens == [
        LaTeXToken('CARET', '^', 0)
    ]


def test_underscore() -> None:
    string = '_'
    tokens = tokenize_latex(string)
    assert tokens == [
        LaTeXToken('UNDERSCORE', '_', 0)
    ]


def test_command() -> None:
    string = '\\sum_{k \\in \\mscrK}'
    tokens = tokenize_latex(string)
    assert tokens == [
        LaTeXToken('BACKSLASH', '\\', 0),
        LaTeXToken('TEXT', 'sum', 1),
        LaTeXToken('UNDERSCORE', '_', 4),
        LaTeXToken('OPENING_BRACE', '{', 5),
        LaTeXToken('TEXT', 'k', 6),
        LaTeXToken('WHITESPACE', ' ', 7),
        LaTeXToken('BACKSLASH', '\\', 8),
        LaTeXToken('TEXT', 'in', 9),
        LaTeXToken('WHITESPACE', ' ', 11),
        LaTeXToken('BACKSLASH', '\\', 12),
        LaTeXToken('TEXT', 'mscrK', 13),
        LaTeXToken('CLOSING_BRACE', '}', 18),
    ]


def test_real() -> None:
    with open(FIGURES_PATH / 'thm__natural_number_divisibility_order.tex') as file:
        string = file.read()
        tokens = tokenize_latex(string)
        assert ''.join(t.value for t in tokens) == string
