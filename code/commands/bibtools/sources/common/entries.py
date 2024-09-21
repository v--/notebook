from notebook.bibtex.author import BibAuthor
from notebook.bibtex.entry import BibEntry
from notebook.math.nlp.rake import RakeNoPhrasesError
from notebook.math.nlp.token_sequence import TokenSequence
from notebook.support.unicode import remove_accents, remove_symbols, remove_whitespace

from .dates import extract_year
from .keywords import generate_keyphrase_scores
from .titles import Titles


def mangle_string_for_entry_name(string: str) -> str:
    return remove_whitespace(remove_symbols(remove_accents(string).title()))


def generate_keyphrase(titles: Titles, language: str, *aux_texts: str | None) -> TokenSequence:
    non_null_aux = [aux for aux in aux_texts if aux]

    try:
        title_scores = generate_keyphrase_scores(titles.main, language, *non_null_aux)
    except RakeNoPhrasesError:
        return TokenSequence([])

    title_keyphrase = title_scores.get_shortest_max_scoring()

    if titles.sub is None:
        return title_keyphrase

    try:
        subtitle_scores = generate_keyphrase_scores(titles.sub, language, *non_null_aux)
    except RakeNoPhrasesError:
        return title_keyphrase

    if title_scores.get_max_score() < subtitle_scores.get_max_score():
        return subtitle_scores.get_shortest_max_scoring()

    return title_keyphrase


def generate_entry_name(author: BibAuthor, year: str | None, titles: Titles, language: str, *aux_texts: str | None) -> str:
    keyphrase = generate_keyphrase(titles, language, *aux_texts)
    mangled_keyphrase = mangle_string_for_entry_name(str(keyphrase))
    mangled_name = mangle_string_for_entry_name(author.main_name)
    return f'{mangled_name}{year or ''}{mangled_keyphrase}'


def regenerate_entry_name(entry: BibEntry, *aux_texts: str | None) -> str:
    titles = Titles(entry.title, entry.subtitle)
    year = extract_year(entry.date)
    return generate_entry_name(entry.authors[0], year, titles, entry.language, *aux_texts)
