
from typing import TYPE_CHECKING

from .rake import generate_phrase_scores


if TYPE_CHECKING:
    from collections.abc import Collection


def test_generate_phrase_scores(fifth_postulate: str, fifth_postulate_stop_words: Collection[str]) -> None:
    scores = generate_phrase_scores(
        fifth_postulate,
        stop_words=fifth_postulate_stop_words,
    )

    top = {str(phrase) for phrase in scores.iter_max_scoring()}
    assert top == {'internal angles'}
