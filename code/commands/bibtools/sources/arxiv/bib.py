import re

from notebook.bibtex.entry import BibEntry
from notebook.support.unicode import normalize_whitespace

from ..common.entries import generate_entry_name
from ..common.names import name_to_bib_author
from ..common.titles import split_title
from .model import ArxivEntry


def arxiv_entry_to_bib(aentry: ArxivEntry, arxiv_id: str) -> BibEntry:
    main_url = aentry.id

    version_match = re.match(r'.+v(?P<version>\d+)', arxiv_id)
    version = int(version_match.group('version')) if version_match else None

    authors = [name_to_bib_author(aauthor.name) for aauthor in aentry.authors]
    year = str(aentry.updated.year)
    date = aentry.updated.to_datetime().strftime('%Y-%m-%d')

    titles = split_title(normalize_whitespace(aentry.title.value))

    # Some arXiv submissions are in other languages, but there is no general way to find out (see 1010.0824v13)
    language = 'english'

    return BibEntry(
        entry_type='article',
        entry_name=generate_entry_name(authors[0], year, titles, language, aentry.summary, aentry.journal_ref),
        authors=authors,
        title=titles.main,
        subtitle=titles.sub,
        language=language,
        archiveprefix='arXiv',
        primaryclass=aentry.primary_category.term,
        eprint=arxiv_id,
        date=date,
        url=main_url,
        edition=str(version) if (version or 0) > 1 else None,
        institution=aentry.affiliation,
        doi=aentry.doi
    )
