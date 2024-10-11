import itertools
from collections.abc import Collection, Iterable, Mapping
from typing import NamedTuple

from ...parsing.whitespace import Whitespace
from .exceptions import NlpError
from .token_sequence import TokenSequence
from .tokens import WordToken


class RakeError(NlpError):
    pass


class RakeNoPhrasesError(NlpError):
    pass


def iter_words(seq: TokenSequence) -> Iterable[WordToken]:
    for token in seq:
        if isinstance(token, WordToken):
            yield token


def iter_phrases(seq: TokenSequence, stop_words: Collection[str]) -> Iterable[TokenSequence]:
    yield from seq.split_by(lambda token: not isinstance(token, WordToken | Whitespace) or str(token).lower() in stop_words)


class WordScoreContext(NamedTuple):
    frequency: Mapping[str, int]
    degree: Mapping[str, int]

    def get_score(self, word: WordToken) -> float:
        key = str(word).lower()

        if key not in self.degree:
            return 0

        return self.degree[key] / self.frequency[key]


def generate_word_score(phrases: Iterable[TokenSequence]) -> WordScoreContext:
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
            degree[key] += (len(words) - 1)

    return WordScoreContext(frequency, degree)


class PhraseScoreContext(NamedTuple):
    scores: Mapping[TokenSequence, float]

    def get_max_score(self) -> float:
        return max(self.scores.values())

    def iter_sorted(self, limit: int | None = None) -> Iterable[tuple[TokenSequence, float]]:
        return itertools.islice(
            sorted(self.scores.items(), key=lambda x: x[1], reverse=True),
            limit
        )

    def iter_max_scoring(self, limit: int | None = None) -> Iterable[TokenSequence]:
        max_score = self.get_max_score()

        for phrase, score in self.iter_sorted(limit):
            if score < max_score:
                return

            yield phrase

    def get_shortest_max_scoring(self) -> TokenSequence:
        return min(
            self.iter_max_scoring(),
            key=lambda phrase: (len(phrase), len(str(phrase)))
        )


def generate_phrase_scores(
    seq: TokenSequence,
    stop_words: Collection[str],
    *aux_seq: TokenSequence
) -> PhraseScoreContext:
    phrases = list(iter_phrases(seq, stop_words))

    if len(phrases) == 0:
        raise RakeNoPhrasesError(f'No phrases found in {str(seq)!r}')

    word_scores = generate_word_score(phrases)

    aux_phrases = itertools.chain(*(iter_phrases(aux, stop_words) for aux in aux_seq))
    aux_word_scores = generate_word_score(aux_phrases)

    phrase_scores = dict[TokenSequence, float]()

    for phrase in phrases:
        phrase_scores.setdefault(phrase, 0.0)

        for token in phrase:
            if isinstance(token, WordToken):
                phrase_scores[phrase] += word_scores.get_score(token) + aux_word_scores.get_score(token)

    return PhraseScoreContext(phrase_scores)

