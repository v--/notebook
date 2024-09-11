from collections.abc import Sequence

import many_stop_words
import stop_words

from notebook.math.nlp.parsing import tokenize_text
from notebook.math.nlp.rake import PhraseScoreContext, generate_phrase_scores

from .languages import get_language_code


def get_stop_words(language: str) -> Sequence[str]:
    lang_code = get_language_code(language)

    # many_stop_words lists korean as 'kr' for some reason
    if lang_code == 'ko':
        lang_code = 'kr'

    if lang_code in many_stop_words.available_languages:
        return many_stop_words.get_stop_words(lang_code)

    if language in stop_words.AVAILABLE_LANGUAGES:
        return stop_words.get_stop_words(language)

    return []


def generate_keyphrase_scores(main_text: str, language: str, *aux_texts: str) -> PhraseScoreContext:
    return generate_phrase_scores(
        tokenize_text(main_text),
        get_stop_words(language),
        *map(tokenize_text, aux_texts)
    )
