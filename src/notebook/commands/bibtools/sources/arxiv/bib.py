import re

from .....bibtex import BibEntry
from .....support.unicode import normalize_whitespace
from ... import url_templates
from ..common.entries import generate_entry_name
from ..common.names import name_to_bib_author
from .model import ArxivEntry


def arxiv_entry_to_bib(aentry: ArxivEntry, arxiv_id: str) -> BibEntry:
    version_match = re.match(r'.+v(?P<version>\d+)', arxiv_id)
    version = int(version_match.group('version')) if version_match else None

    authors = [name_to_bib_author(aauthor.name) for aauthor in aentry.authors]
    year = str(aentry.updated.year)
    date = aentry.updated.to_datetime().strftime('%Y-%m-%d')

    # Some arXiv submissions are in other languages, but there is no general way to find out (see 1010.0824v13)
    language = 'english'
    title = normalize_whitespace(aentry.title.value)

    return BibEntry(
        entry_type='misc',
        entry_name=generate_entry_name(authors, year, title, language, aentry.summary, aentry.journal_ref),
        authors=authors,
        title=title,
        languages=[language],
        eprinttype='arXiv',
        eprintclass=aentry.primary_category.term,
        eprint=arxiv_id,
        date=date,
        edition=str(version) if (version or 0) > 1 else None,
        institution=aentry.affiliation,
        doi=url_templates.clean_identifier(aentry.doi, url_templates.doi)
    )
