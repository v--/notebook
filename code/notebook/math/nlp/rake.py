import itertools
from collections.abc import Collection, Iterable, Mapping
from typing import NamedTuple

from ...parsing.whitespace import Whitespace
from .token_sequence import TokenSequence
from .tokens import WordToken


def iter_words(seq: TokenSequence) -> Iterable[WordToken]:
    for token in seq:
        if isinstance(token, WordToken):
            yield token


def iter_phrases(seq: TokenSequence, stop_words: Collection[str]) -> Iterable[TokenSequence]:
    yield from seq.split_by(lambda token: not isinstance(token, WordToken | Whitespace) or str(token).lower() in stop_words)


class WordScoreContext(NamedTuple):
    frequency: dict[str, int]
    degree: dict[str, int]

    def get_score(self, word: WordToken) -> float:
        key = str(word).lower()
        return self.degree[key] / self.frequency[key]


def generate_word_score(phrases: Iterable[TokenSequence], additional_phrases: Iterable[TokenSequence] | None = None) -> WordScoreContext:
    frequency = dict[str, int]()
    # The degree of a word is the sum of lengths of all phrases it occurs in minus the number of phrases.
    # This is the degree of the word in the adjacency graph if we count all words within a phrase as adjacent.
    # We inflate this degree with additional phrases
    degree = dict[str, int]()

    for phrase in phrases:
        words = list(iter_words(phrase))

        for word in words:
            key = str(word).lower()
            frequency.setdefault(key, 0)
            frequency[key] += 1
            degree.setdefault(key, 0)
            degree[key] += len(words) - 1

    if additional_phrases:
        for phrase in additional_phrases:
            words = list(iter_words(phrase))

            for word in words:
                key = str(word).lower()

                if key in degree:
                    degree[key] += len(words) - 1

    return WordScoreContext(frequency, degree)


class PhraseScoreContext(NamedTuple):
    scores: Mapping[TokenSequence, float]

    def iter_sorted(self, limit: int | None = None) -> Iterable[tuple[TokenSequence, float]]:
        return itertools.islice(
            sorted(self.scores.items(), key=lambda x: x[1], reverse=True),
            limit
        )

    def iter_max_scoring(self, limit: int | None = None) -> Iterable[TokenSequence]:
        max_score = 0.0

        for phrase, score in self.iter_sorted(limit):
            if max_score == 0:
                max_score = score
            elif score < max_score:
                return

            yield phrase


def generate_phrase_scores(
    seq: TokenSequence,
    stop_words: Collection[str],
    additional_training: TokenSequence | None = None
) -> PhraseScoreContext:
    phrases = list(iter_phrases(seq, stop_words))
    additional_phrases = list(iter_phrases(additional_training, stop_words)) if additional_training else []
    word_score_context = generate_word_score(phrases, additional_phrases=additional_phrases)
    phrase_scores = dict[TokenSequence, float]()

    for phrase in phrases:
        phrase_scores.setdefault(phrase, 0.0)

        for token in phrase:
            if isinstance(token, WordToken):
                phrase_scores[phrase] += word_score_context.get_score(token)

    return PhraseScoreContext(phrase_scores)

