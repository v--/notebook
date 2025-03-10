import itertools
from collections.abc import Collection, Iterable, Mapping
from dataclasses import dataclass

from .exceptions import NlpError
from .parsing import extract_phrases
from .phrases import Phrase


class RakeError(NlpError):
    pass


class RakeNoPhrasesError(NlpError):
    pass


@dataclass(frozen=True)
class WordScoreContext:
    frequency: Mapping[str, int]
    degree: Mapping[str, int]

    def get_score(self, word: str) -> float:
        key = word.lower()

        if key not in self.degree:
            return 0.0

        return self.degree[key] / self.frequency[key]


def generate_word_score(phrases: Iterable[Phrase]) -> WordScoreContext:
    frequency = dict[str, int]()
    # The degree of a word is the sum of lengths of all phrases it occurs in minus the number of phrases.
    # This is the degree of the word in the adjacency graph if we count all words within a phrase as adjacent.
    # We inflate this degree with additional phrases
    degree = dict[str, int]()

    for phrase in phrases:
        for word in phrase:
            key = word.lower()
            frequency.setdefault(key, 0)
            frequency[key] += 1
            degree.setdefault(key, 0)
            degree[key] += (len(phrase) - 1)

    return WordScoreContext(frequency, degree)


@dataclass(frozen=True)
class PhraseScoreContext:
    scores: Mapping[Phrase, float]

    def get_max_score(self) -> float:
        return max(self.scores.values())

    def iter_sorted(self, limit: int | None = None) -> Iterable[tuple[Phrase, float]]:
        return itertools.islice(
            sorted(self.scores.items(), key=lambda x: x[1], reverse=True),
            limit
        )

    def iter_max_scoring(self, limit: int | None = None) -> Iterable[Phrase]:
        max_score = self.get_max_score()

        for phrase, score in self.iter_sorted(limit):
            if score < max_score:
                return

            yield phrase

    def get_shortest_max_scoring(self) -> Phrase:
        return min(
            self.iter_max_scoring(),
            key=lambda phrase: (len(phrase), len(str(phrase)))
        )


def generate_phrase_scores(
    main_text: str,
    stop_words: Collection[str],
    *aux_texts: str
) -> PhraseScoreContext:
    phrases = extract_phrases(main_text, stop_words)

    if len(phrases) == 0:
        raise RakeNoPhrasesError(f'No phrases found in {str(main_text)!r}')

    word_scores = generate_word_score(phrases)

    aux_phrases = itertools.chain(*(extract_phrases(aux, stop_words) for aux in aux_texts))
    aux_word_scores = generate_word_score(aux_phrases)

    phrase_scores = dict[Phrase, float]()

    for phrase in phrases:
        phrase_scores.setdefault(phrase, 0.0)

        for word in phrase:
            phrase_scores[phrase] += word_scores.get_score(word) + aux_word_scores.get_score(word)

    return PhraseScoreContext(phrase_scores)
