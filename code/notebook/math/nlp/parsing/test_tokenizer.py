from ....parsing.whitespace import Whitespace
from ..token_sequence import TokenSequence
from ..tokens import NumberToken, SymbolToken, WordToken
from .tokenizer import tokenize_text


def test_english_word() -> None:
    assert tokenize_text('Test') == TokenSequence([WordToken('Test')])


def test_standalone_apostrophe() -> None:
    assert tokenize_text("'") == TokenSequence([SymbolToken("'")])


def test_english_word_with_apostrophe() -> None:
    assert tokenize_text("Can't") == TokenSequence([WordToken("Can't")])


def test_standalone_dash() -> None:
    assert tokenize_text('-') == TokenSequence([SymbolToken('-')])


def test_english_word_with_dash() -> None:
    assert tokenize_text('Semi-demigod') == TokenSequence([WordToken('Semi-demigod')])


def test_english_phrase() -> None:
    assert tokenize_text('Waters rising') == TokenSequence([
        WordToken('Waters'), Whitespace.space, WordToken('rising')
    ])


def test_spaces_preserved() -> None:
    assert tokenize_text('Waters  rising ') == TokenSequence([
        WordToken('Waters'), Whitespace.space, Whitespace.space, WordToken('rising'), Whitespace.space
    ])


def test_english_sentence() -> None:
    assert tokenize_text('Water is rising, coming to wash it all away.') == TokenSequence([
        WordToken('Water'),  Whitespace.space,
        WordToken('is'),     Whitespace.space,
        WordToken('rising'),
        SymbolToken(','),    Whitespace.space,
        WordToken('coming'), Whitespace.space,
        WordToken('to'),     Whitespace.space,
        WordToken('wash'),   Whitespace.space,
        WordToken('it'),     Whitespace.space,
        WordToken('all'),    Whitespace.space,
        WordToken('away'),
        SymbolToken('.')
    ])


def test_number() -> None:
    assert tokenize_text('314') == TokenSequence([NumberToken('314')])


def test_numeric_prefix() -> None:
    assert tokenize_text('314-partite') == TokenSequence([WordToken('314-partite')])


def test_cyrillic_word() -> None:
    assert tokenize_text('Тест') == TokenSequence([WordToken('Тест')])


def test_cyrillic_sentence() -> None:
    assert tokenize_text('Сморкалось.') == TokenSequence([WordToken('Сморкалось'), SymbolToken('.')])


def test_unicode() -> None:
    assert tokenize_text('Matrichnyĭ analiz i lineĭnai͡a algebra') == TokenSequence([
        WordToken('Matrichnyĭ'), Whitespace.space,
        WordToken('analiz'),     Whitespace.space,
        WordToken('i'),          Whitespace.space,
        WordToken('lineĭnai͡a'),  Whitespace.space,
        WordToken('algebra')
    ])


def test_space_separator() -> None:
    assert tokenize_text('de Beer') == TokenSequence([
        WordToken('de'),  Whitespace.space,
        WordToken('Beer')
    ])
