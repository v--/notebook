from collections.abc import Sequence

import stop_words

from .....math.nlp.rake import PhraseScoreContext, generate_phrase_scores


def get_stop_words(language: str) -> Sequence[str]:
    if language in stop_words.AVAILABLE_LANGUAGES:
        return stop_words.get_stop_words(language)

    return []


def generate_keyphrase_scores(main_text: str, language: str, *aux_texts: str) -> PhraseScoreContext:
    return generate_phrase_scores(
        main_text,
        get_stop_words(language),
        *aux_texts
    )
