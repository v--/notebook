from collections.abc import Sequence

import many_stop_words
import stop_words
from iso639 import Lang

from notebook.math.nlp.parsing import tokenize_text
from notebook.math.nlp.rake import generate_phrase_scores
from notebook.support.unicode import normalize_whitespace


def get_stop_words(language: str) -> Sequence[str]:
    lang = Lang(language.title())
    # many_stop_words lists korean as 'kr' for some reason
    lang_code = lang.pt1 if language != 'korean' else 'kr'

    if lang_code in many_stop_words.available_languages:
        return many_stop_words.get_stop_words(lang_code)

    if language in stop_words.AVAILABLE_LANGUAGES:
        return stop_words.get_stop_words(language)

    return []


def extract_keyphrase(main_text: str, language: str, *aux_texts: str) -> str:
    scores = generate_phrase_scores(
        tokenize_text(main_text),
        get_stop_words(language),
        *map(tokenize_text, aux_texts)
    )

    min_len_top_phrase = min(
        (phrase for phrase in scores.iter_max_scoring() if any(len(str(token)) > 2 for token in phrase)),
        key=lambda phrase: (len(phrase), len(str(phrase)))
    )

    return normalize_whitespace(str(min_len_top_phrase))
