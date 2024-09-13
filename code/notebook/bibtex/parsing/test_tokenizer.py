from ...parsing.whitespace import Whitespace
from .tokenizer import tokenize_bibtex
from .tokens import NumberToken, WordToken


def test_empty_string() -> None:
    string = ''
    tokens = tokenize_bibtex(string)
    assert tokens == []


def test_latin_token() -> None:
    string = 'latin'
    tokens = tokenize_bibtex(string)
    assert tokens == [WordToken(string)]


def test_latin_name() -> None:
    string = 'Svatopluk Fučík'
    tokens = tokenize_bibtex(string)
    assert tokens == [WordToken('Svatopluk'), Whitespace.space, WordToken('Fučík')]


def test_cyrillic_token() -> None:
    string = 'кириллица'
    tokens = tokenize_bibtex(string)
    assert tokens == [WordToken(string)]


def test_cyrillic_name() -> None:
    string = 'Андрей Петрович Киселёв'
    tokens = tokenize_bibtex(string)
    assert tokens == [WordToken('Андрей'), Whitespace.space, WordToken('Петрович'), Whitespace.space, WordToken('Киселёв')]


def test_number_token() -> None:
    string = '00'
    tokens = tokenize_bibtex(string)
    assert tokens == [NumberToken(string)]
