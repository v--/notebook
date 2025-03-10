from .tokenizer import tokenize_text
from .tokens import TextToken


def test_english_word() -> None:
    assert tokenize_text('Test') == [
        TextToken('WORD', 'Test', 0)
    ]


def test_standalone_apostrophe() -> None:
    assert tokenize_text("'") == [
        TextToken('SYMBOL', "'", 0)
    ]


def test_english_word_with_apostrophe() -> None:
    assert tokenize_text("Can't") == [
        TextToken('WORD', "Can't", 0)
    ]


def test_standalone_dash() -> None:
    assert tokenize_text('-') == [
        TextToken('SYMBOL', '-', 0)
    ]


def test_english_word_with_dash() -> None:
    assert tokenize_text('Semi-demigod') == [
        TextToken('WORD', 'Semi-demigod', 0)
    ]


def test_english_phrase() -> None:
    assert tokenize_text('Waters rising') == [
        TextToken('WORD', 'Waters', 0),
        TextToken('WORD',  'rising', 7)
    ]


def test_spaces_preserved() -> None:
    assert tokenize_text('Waters  rising ') == [
            TextToken('WORD', 'Waters', 0),
            TextToken('WORD', 'rising', 8),
    ]


def test_english_sentence() -> None:
    assert tokenize_text('Water is rising, coming to wash it all away.') == [
        TextToken('WORD', 'Water', 0),
        TextToken('WORD', 'is', 6),
        TextToken('WORD', 'rising', 9),
        TextToken('SYMBOL', ',', 15),
        TextToken('WORD', 'coming', 17),
        TextToken('WORD', 'to', 24),
        TextToken('WORD', 'wash', 27),
        TextToken('WORD', 'it', 32),
        TextToken('WORD', 'all', 35),
        TextToken('WORD', 'away', 39),
        TextToken('SYMBOL', '.', 43)
    ]


def test_decimal() -> None:
    assert tokenize_text('314') == [
        TextToken('DECIMAL', '314', 0)
    ]


def test_decimal_prefix() -> None:
    assert tokenize_text('314-partite') == [
        TextToken('WORD', '314-partite', 0)
    ]


def test_cyrillic_word() -> None:
    assert tokenize_text('Тест') == [
        TextToken('WORD', 'Тест', 0)
    ]


def test_cyrillic_sentence() -> None:
    assert tokenize_text('Сморкалось.') == [
        TextToken('WORD', 'Сморкалось', 0),
        TextToken('SYMBOL', '.', 10)
    ]


def test_bad_unicode() -> None:
    assert tokenize_text('Matrichnyĭ analiz i lineĭnai͡a algebra') == [
        TextToken('WORD', 'Matrichnyĭ', 0),
        TextToken('WORD', 'analiz', 11),
        TextToken('WORD', 'i', 18),
        TextToken('WORD', 'lineĭnai͡a', 20),
        TextToken('WORD', 'algebra', 31)
    ]


def test_space_separator() -> None:
    assert tokenize_text('de\xa0Beer') == [
        TextToken('WORD', 'de', 0),
        TextToken('WORD', 'Beer', 3)
    ]
