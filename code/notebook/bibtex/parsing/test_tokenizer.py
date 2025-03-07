from .tokenizer import tokenize_bibtex
from .tokens import BibToken


def test_empty_string() -> None:
    string = ''
    tokens = tokenize_bibtex(string)
    assert tokens == []


def test_latin_token() -> None:
    string = 'latin'
    tokens = tokenize_bibtex(string)
    assert tokens == [
        BibToken('WORD', string, 0)
    ]


def test_latin_name() -> None:
    string = 'Svatopluk Fučík'
    tokens = tokenize_bibtex(string)
    assert tokens == [
        BibToken('WORD', 'Svatopluk', 0),
        BibToken('SPACE', ' ', 9),
        BibToken('WORD', 'Fučík', 10)
    ]


def test_cyrillic_token() -> None:
    string = 'кириллица'
    tokens = tokenize_bibtex(string)
    assert tokens == [BibToken('WORD', string, 0)]


def test_cyrillic_name() -> None:
    string = 'Андрей Петрович Киселёв'
    tokens = tokenize_bibtex(string)
    assert tokens == [
        BibToken('WORD', 'Андрей', 0),
        BibToken('SPACE', ' ', 6),
        BibToken('WORD', 'Петрович', 7),
        BibToken('SPACE', ' ', 15),
        BibToken('WORD', 'Киселёв', 16)
    ]


def test_number_token() -> None:
    string = '00'
    tokens = tokenize_bibtex(string)
    assert tokens == [
        BibToken('NUMBER', '00', 0),
    ]
