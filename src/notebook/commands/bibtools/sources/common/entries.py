import re
from collections.abc import Iterable, Sequence

from .....bibtex.author import BibAuthor
from .....bibtex.entry import BibEntry
from .....bibtex.string import strip_braces
from .....math.nlp.phrases import Phrase
from .....math.nlp.rake import RakeNoPhrasesError
from .....support.iteration import string_accumulator
from .dates import extract_year
from .keywords import generate_keyphrase_scores
from .names import get_main_human_name


@string_accumulator()
def capitalize_first(string: str) -> Iterable[str]:
    for sub in re.split(r'[^\w]+', string):
        if len(sub) > 0:
            yield sub[0].upper()
            yield sub[1:]


def mangle_string_for_entry_name(string: str) -> str:
    return capitalize_first(string)


def generate_keyphrase(title: str, subtitle: str | None, language: str, *aux_texts: str | None) -> Phrase:
    non_null_aux = [aux for aux in aux_texts if aux]

    try:
        title_scores = generate_keyphrase_scores(strip_braces(title), language, *non_null_aux)
    except RakeNoPhrasesError:
        return Phrase([])

    title_keyphrase = title_scores.get_shortest_max_scoring()

    if subtitle is None:
        return title_keyphrase

    try:
        subtitle_scores = generate_keyphrase_scores(strip_braces(subtitle), language, *non_null_aux)
    except RakeNoPhrasesError:
        return title_keyphrase

    if title_scores.get_max_score() < subtitle_scores.get_max_score():
        return subtitle_scores.get_shortest_max_scoring()

    return title_keyphrase


def generate_entry_short_name(
    title: str,
    main_language: str,
    *aux_texts: str | None,
    subtitle: str | None = None,
) -> str:
    keyphrase = generate_keyphrase(title, subtitle, main_language, *aux_texts)
    return mangle_string_for_entry_name(str(keyphrase))


@string_accumulator()
def generate_entry_name(
    authors: Sequence[BibAuthor],
    year: str | None,
    title: str,
    main_language: str,
    *aux_texts: str | None,
    subtitle: str | None = None,
    editors: Sequence[BibAuthor] = [],
) -> Iterable[str]:
    visible_authors = authors or editors

    if len(visible_authors) > 0:
        yield mangle_string_for_entry_name(strip_braces(get_main_human_name(visible_authors[0].full_name)))

    if (len(authors) == 0 and len(editors) > 0) or len(visible_authors) > 2 or (len(visible_authors) == 2 and visible_authors[1] == BibAuthor(full_name='others')):
        yield 'ИПр' if main_language == 'russian' or main_language == 'bulgarian' else 'EtAl'
    elif len(authors) > 1:
        yield mangle_string_for_entry_name(strip_braces(get_main_human_name(visible_authors[1].full_name)))

    if year:
        yield year

    yield generate_entry_short_name(title, main_language, *aux_texts, subtitle=subtitle)


def regenerate_entry_name(entry: BibEntry, main_language: str, *aux_texts: str | None) -> str:
    year = extract_year(strip_braces(entry.date)) if entry.date else None
    return generate_entry_name(
        entry.authors,
        year,
        strip_braces(entry.title),
        main_language,
        *aux_texts,
        editors=entry.editors,
        subtitle=strip_braces(entry.subtitle) if entry.subtitle else None
    )
