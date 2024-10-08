from collections.abc import Collection

from ...parsing.whitespace import Whitespace
from .rake import generate_phrase_scores, iter_phrases
from .token_sequence import TokenSequence
from .tokens import WordToken


def test_iter_phrases(quick_fox: TokenSequence) -> None:
    phrases = list(iter_phrases(quick_fox, stop_words=['the', 'fox']))

    assert phrases == [
        TokenSequence([WordToken('quick'), Whitespace.space, WordToken('brown')]),
        TokenSequence([WordToken('jumps'), Whitespace.space, WordToken('over')]),
        TokenSequence([WordToken('lazy'), Whitespace.space, WordToken('dog')])
    ]


def test_generate_phrase_scores(fifth_postulate: TokenSequence, fifth_postulate_stop_words: Collection[str]) -> None:
    scores = generate_phrase_scores(
        fifth_postulate,
        stop_words=fifth_postulate_stop_words
    )

    top = {str(phrase) for phrase in scores.iter_max_scoring()}
    assert top == {'internal angles'}
