import re

from notebook.bibtex.entry import BibEntry
from notebook.support.unicode import normalize_whitespace

from ...exceptions import BibToolsParseError
from ..common.keywords import generate_entry_name
from ..common.names import name_to_bib_author
from .model import ArxivEntry


def arxiv_entry_to_bib(aentry: ArxivEntry) -> BibEntry:
    id_match = re.match(r'http://arxiv.org/abs/(?P<id>.+)', aentry.id)

    if id_match is None:
        raise BibToolsParseError(f'Could not determine the arXiv identifier from {aentry.id!r}')

    identifier = id_match.group('id')
    main_url = aentry.id

    version_match = re.match(r'.+v(?P<version>\d+)', identifier)
    version = int(version_match.group('version')) if version_match else None

    authors = [name_to_bib_author(aauthor.name) for aauthor in aentry.authors]
    year = str(aentry.updated.year)

    return BibEntry(
        entry_type='article',
        entry_name=generate_entry_name(authors[0], year, aentry.title.value, 'en'),
        authors=authors,
        title=normalize_whitespace(aentry.title.value),
        language='english',  # Some arXiv submissions are in other languages, but there is no general way to find out (see 1010.0824v13)
        archiveprefix='arXiv',
        primaryclass=aentry.primary_category.term,
        eprint=identifier,
        year=year,
        url=main_url,
        edition=str(version) if (version or 0) > 1 else None,
        institution=aentry.affiliation,
        journal=aentry.journal_ref,
        doi=aentry.doi
    )
