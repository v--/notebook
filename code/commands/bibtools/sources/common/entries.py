from notebook.bibtex.author import BibAuthor
from notebook.support.unicode import remove_accents, remove_symbols, remove_whitespace

from .keywords import generate_keyphrase_scores
from .titles import Titles


def mangle_string_for_entry_name(string: str) -> str:
    return remove_whitespace(remove_symbols(remove_accents(string).title()))


def generate_entry_name(author: BibAuthor, year: str, titles: Titles, language: str, *aux_texts: str | None) -> str:
    non_null_aux = [aux for aux in aux_texts if aux]
    title_scores = generate_keyphrase_scores(titles.main, language, *non_null_aux)
    keyphrase = title_scores.get_shortest_max_scoring()

    if titles.sub is not None:
        subtitle_scores = generate_keyphrase_scores(titles.sub, language, *non_null_aux)

        if title_scores.get_max_score() < subtitle_scores.get_max_score():
            keyphrase = subtitle_scores.get_shortest_max_scoring()

    mangled_keyphrase = mangle_string_for_entry_name(str(keyphrase))
    mangled_name = mangle_string_for_entry_name(author.main_name)
    return f'{mangled_name}{year}{mangled_keyphrase}'
