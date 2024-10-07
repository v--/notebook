import re
from collections.abc import Iterable, Sequence

from notebook.bibtex.author import BibAuthor
from notebook.bibtex.entry import BibEntry
from notebook.bibtex.string import strip_braces
from notebook.math.nlp.rake import RakeNoPhrasesError
from notebook.math.nlp.token_sequence import TokenSequence
from notebook.support.iteration import string_accumulator
from notebook.support.unicode import remove_accents

from .dates import extract_year
from .keywords import generate_keyphrase_scores
from .names import get_main_human_name
from .titles import Titles


@string_accumulator()
def capitalize_first(string: str) -> Iterable[str]:
    for sub in re.split(r'[^\w]+', string):
        if len(sub) > 0:
            yield sub[0].upper()
            yield sub[1:]


def mangle_string_for_entry_name(string: str) -> str:
    return remove_accents(capitalize_first(string))


def generate_keyphrase(titles: Titles, language: str, *aux_texts: str | None) -> TokenSequence:
    non_null_aux = [aux for aux in aux_texts if aux]

    try:
        title_scores = generate_keyphrase_scores(strip_braces(titles.main), language, *non_null_aux)
    except RakeNoPhrasesError:
        return TokenSequence([])

    title_keyphrase = title_scores.get_shortest_max_scoring()

    if titles.sub is None:
        return title_keyphrase

    try:
        subtitle_scores = generate_keyphrase_scores(strip_braces(titles.sub), language, *non_null_aux)
    except RakeNoPhrasesError:
        return title_keyphrase

    if title_scores.get_max_score() < subtitle_scores.get_max_score():
        return subtitle_scores.get_shortest_max_scoring()

    return title_keyphrase


@string_accumulator()
def generate_entry_name(authors: Sequence[BibAuthor], year: str | None, titles: Titles, language: str, *aux_texts: str | None) -> Iterable[str]:
    if len(authors) > 0:
        yield mangle_string_for_entry_name(strip_braces(get_main_human_name(authors[0].full_name)))

    if len(authors) > 2 or (len(authors) == 2 and authors[1] == BibAuthor(full_name='others')):
        yield 'ИПр' if language == 'russian' or language == 'bulgarian' else 'EtAl'
    elif len(authors) > 1:
        yield mangle_string_for_entry_name(strip_braces(get_main_human_name(authors[1].full_name)))

    if year:
        yield year

    keyphrase = generate_keyphrase(titles, language, *aux_texts)
    yield mangle_string_for_entry_name(str(keyphrase))


def regenerate_entry_name(entry: BibEntry, *aux_texts: str | None) -> str:
    titles = Titles(entry.title, entry.subtitle)
    year = extract_year(strip_braces(entry.date)) if entry.date else None
    return generate_entry_name(entry.authors or entry.editors, year, titles, entry.language, *aux_texts)
