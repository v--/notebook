from ..phrases import Phrase
from .parser import extract_phrases


def test_extract_phrases_quick_fox(quick_fox: str) -> None:
    phrases = extract_phrases(quick_fox, stop_words=['the', 'fox'])

    assert phrases == [
        Phrase(['quick', 'brown']),
        Phrase(['jumps', 'over']),
        Phrase(['lazy', 'dog'])
    ]


def test_extract_phrases_henkin() -> None:
    phrases = extract_phrases('Completeness in the theory of types', stop_words=['in', 'the', 'of'])

    assert phrases == [
        Phrase(['Completeness']),
        Phrase(['theory']),
        Phrase(['types'])
    ]

