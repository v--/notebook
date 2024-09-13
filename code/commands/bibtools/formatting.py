from typing import Any, TextIO

import loguru
from stdnum import isbn, issn

from notebook.bibtex.author import BibAuthor
from notebook.bibtex.entry import BibEntry
from notebook.bibtex.parsing import parse_bibtex
from notebook.parsing.parser import ParsingError

from ..common.formatting import Formatter
from ..common.names import latinize_cyrillic_name
from .exceptions import BibToolsParsingError
from .sources.common.languages import normalize_language_name


class BibFormatter(Formatter):
    def get_sublogger(self, entry: BibEntry) -> 'loguru.Logger':
        return self.logger.bind(logger=self.path.name + ':' + entry.entry_name)

    def adjust_author(self, author: BibAuthor, entry: BibEntry) -> BibAuthor:
        adjusted = author

        if adjusted.display_name is None and (entry.language == 'russian' or entry.language == 'bulgarian'):
            self.get_sublogger(entry).info('Adding Latinized names')
            adjusted = adjusted._replace(display_name=latinize_cyrillic_name(adjusted.get_shortened_string()))

        return adjusted

    def warn_of_blank_field(self, entry: BibEntry, field_name: str) -> None:
        if getattr(entry, field_name) is None:
            self.logger.bind(logger=entry.entry_name).warning(f'The field {field_name} is blank')

    def adjust_field(self, entry: BibEntry, field_name: str, new_value: Any) -> BibEntry:  # noqa: ANN401
        old_value = getattr(entry, field_name)

        if old_value != new_value:
            self.get_sublogger(entry).info(f'Updating the {field_name} field from {old_value!r} to {new_value!r}')
            return entry._replace(**{field_name: new_value})

        return entry

    def adjust_entry_date(self, entry: BibEntry) -> BibEntry:
        if entry.date is not None:
            return entry

        if entry.year is None:
            self.warn_of_blank_field(entry, 'date')
            return entry

        self.get_sublogger(entry).info("Moving the 'year' field to 'date'")

        date = entry.year
        entry = entry._replace(year=None)

        if entry.month:
            date += '-' + entry.month

        if entry.day:
            date += '-' + entry.day

        return entry._replace(date=date, year=None, month=None, day=None)

    def adjust_entry(self, entry: BibEntry) -> BibEntry:
        adjusted = entry
        adjusted._replace(authors=[self.adjust_author(author, adjusted) for author in adjusted.authors])

        adjusted = self.adjust_field(adjusted, 'language', normalize_language_name(adjusted.language))
        adjusted = self.adjust_field(adjusted, 'isbn', isbn.format(adjusted.isbn) if adjusted.isbn else None)
        adjusted = self.adjust_field(adjusted, 'issn', issn.format(adjusted.issn) if adjusted.issn else None)
        adjusted = self.adjust_entry_date(adjusted)

        return adjusted

    def format(self, src: TextIO, dest: TextIO) -> None:
        try:
            entries = parse_bibtex(src.read())
        except ParsingError as err:
            raise BibToolsParsingError(str(err) + '\n\n' + err.__notes__[0]) from err

        for i, entry in enumerate(entries):
            adjusted = self.adjust_entry(entry)
            dest.write(str(adjusted))

            if i + 1 < len(entries):
                dest.write('\n')
