from many_stop_words import get_stop_words

from notebook.bibtex.author import BibAuthor
from notebook.math.nlp.parsing import tokenize_text
from notebook.math.nlp.rake import generate_phrase_scores
from notebook.support.unicode import normalize_whitespace, remove_accents, remove_symbols, remove_whitespace


def extract_keyphrase(text: str, language: str) -> str:
    scores = generate_phrase_scores(
        tokenize_text(text),
        get_stop_words(language),
        max_len=2
    )

    min_len_top_phrase = min(
        scores.iter_max_scoring(),
        key=lambda phrase: (len(phrase), len(str(phrase)))
    )

    return normalize_whitespace(str(min_len_top_phrase))


def mangle_string_for_entry_name(string: str) -> str:
    return remove_whitespace(remove_symbols(remove_accents(string)).title())


def generate_entry_name(author: BibAuthor, year: str, summary: str, language: str) -> str:
    keyphrase = extract_keyphrase(summary, language)
    mangled_keyphrase = mangle_string_for_entry_name(keyphrase)
    mangled_name = mangle_string_for_entry_name(author.main_name)
    return f'{mangled_name}{year}{mangled_keyphrase}'
