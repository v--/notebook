import itertools
from collections.abc import Collection, Iterable, Mapping
from typing import NamedTuple

from ...parsing.whitespace import Whitespace
from .token_sequence import TokenSequence
from .tokens import TextToken, WordToken


def iter_phrases(seq: TokenSequence, stop_words: Collection[str], *, max_len: int | None = None, split_at_line_break: bool = False) -> Iterable[TokenSequence]:
    def predicate(token: TextToken) -> bool:
        if split_at_line_break and token == Whitespace.line_break:
            return True

        if not isinstance(token, WordToken | Whitespace):
            return True

        return str(token).lower() in stop_words

    if max_len is None:
        yield from seq.split_by(predicate)
        return

    for phrase in seq.split_by(predicate):
        for i in range(max(1, len(phrase) - max_len)):
            if not isinstance(phrase[i], WordToken):
                continue

            buffer = list[TextToken]()
            word_count = 0

            for token in phrase[i:]:
                if isinstance(token, WordToken):
                    word_count += 1

                if word_count > 0:
                    buffer.append(token)

                if word_count == max_len:
                    break

            if word_count > 0:
                yield TokenSequence(buffer)


class WordScoreContext(NamedTuple):
    frequency: dict[str, int]
    degree: dict[str, int]

    def get_score(self, word: WordToken) -> float:
        key = str(word).lower()
        return self.degree[key] / self.frequency[key]


def generate_word_score(phrases: Iterable[TokenSequence]) -> WordScoreContext:
    frequency = dict[str, int]()
    # The degree of a word is the sum of lengths of all phrases it occurs in minus the number of phrases.
    # This is the degree of the word in the adjacency graph if we count all words within a phrase as adjacent.
    degree = dict[str, int]()

    for phrase in phrases:
        words = [token for token in phrase if isinstance(token, WordToken)]

        for word in words:
            key = str(word).lower()
            frequency.setdefault(key, 0)
            frequency[key] += 1
            degree.setdefault(key, 0)
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


def generate_phrase_scores(seq: TokenSequence, stop_words: Collection[str], *, max_len: int | None = None, split_at_line_break: bool = False) -> PhraseScoreContext:
    phrases = list(iter_phrases(seq, stop_words, max_len=max_len, split_at_line_break=split_at_line_break))
    word_score_context = generate_word_score(phrases)
    phrase_scores = dict[TokenSequence, float]()

    for phrase in phrases:
        phrase_scores.setdefault(phrase, 0.0)

        for token in phrase:
            if isinstance(token, WordToken):
                phrase_scores[phrase] += word_score_context.get_score(token)

    return PhraseScoreContext(phrase_scores)

