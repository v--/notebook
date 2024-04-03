import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
from titlecase import titlecase
from typing import TextIO

from .names import latinize_cyrillic_name
from ..common.formatting import Formatter


def titlecase_bib_callback(string: str, **kwargs) -> str | None:
    if not string.isascii() or string == string.upper():
        return string

    return None


class BibFormatter(Formatter):
    def format(self, src: TextIO, dest: TextIO) -> None:
        parser = BibTexParser(ignore_nonstandard_types=False)
        bibtex_db = bibtexparser.load(src, parser)

        bibtex_db.entries = sorted(
            bibtex_db.entries,
            key=lambda entry: entry['ID']
        )

        for entry in bibtex_db.entries:
            if entry['ENTRYTYPE'] != 'online':
                for field in ['title', 'subtitle']:
                    if field not in entry:
                        continue

                    title_cased = titlecase(entry[field], callback=titlecase_bib_callback)

                    if title_cased:
                        entry[field] = title_cased

            if 'shortauthor' in entry:
                continue

            if entry['language'] == 'russian' or entry['language'] == 'bulgarian':
                entry['shortauthor'] = ' and '.join(
                    latinize_cyrillic_name(author) for author in entry['author'].split(' and ')
                )

        writer = BibTexWriter()
        writer.indent = '  '

        dest.write(writer.write(bibtex_db))
