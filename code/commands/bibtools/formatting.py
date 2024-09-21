from collections.abc import Sequence
from typing import Any, TextIO

import loguru
from stdnum import isbn, issn

from notebook.bibtex.author import BibAuthor
from notebook.bibtex.entry import BibEntry
from notebook.bibtex.parsing import parse_bibtex
from notebook.parsing.parser import ParsingError

from ..common.names import latinize_cyrillic_name
from .exceptions import BibToolsParsingError
from .sources.common.languages import normalize_language_name
from .sources.common.names import name_to_bib_author
from .sources.common.titles import split_title


class BibEntryAdjuster:
    original: BibEntry
    logger: 'loguru.Logger'

    def __init__(self, entry: BibEntry, logger: 'loguru.Logger') -> None:
        self.original = entry
        self.adjusted = entry
        self.logger = logger

    def update(self, **kwargs: Any) -> None:  # noqa: ANN401
        for field_name, new_value in kwargs.items():
            old_value = getattr(self.adjusted, field_name)

            if old_value != new_value:
                if new_value is None:
                    self.logger.info(f'Removing the {field_name} field')
                elif old_value is None:
                    self.logger.info(f'Setting the {field_name} field to {new_value!r}')
                else:
                    self.logger.info(f'Updating the {field_name} field from {old_value!r} to {new_value!r}')

        self.adjusted = self.adjusted._replace(**kwargs)

    def get_author_display_name(self, author: BibAuthor) -> str | None:
        if author.display_name is None and (self.adjusted.language == 'russian' or self.adjusted.language == 'bulgarian'):
            return latinize_cyrillic_name(author.main_name)

        return author.display_name

    def adjust_author(self, author: BibAuthor) -> BibAuthor:
        if author.verbatim:
            adjusted = author
        else:
            adjusted = name_to_bib_author(author.get_full_string())._replace(display_name=author.display_name)

        if adjusted != author:
            self.logger.info(f'Updating author name from {author.get_full_string()!r} to {adjusted.get_full_string()!r}')

        display_name = self.get_author_display_name(adjusted)

        if author.display_name != display_name:
            self.logger.info(f'Updating author display name from {adjusted.display_name!r} to {display_name!r}')

        return adjusted._replace(display_name=display_name)

    def adjust_entry_date(self) -> None:
        if self.adjusted.date is not None:
            return

        if self.adjusted.year is None:
            self.logger.warning('The date field is blank')
            return

        date = self.adjusted.year

        if self.adjusted.month:
            date += '-' + self.adjusted.month.rjust(2, '0')

        if self.adjusted.day:
            date += '-' + self.adjusted.day.rjust(2, '0')

        self.update(date=date, year=None, month=None, day=None)

    def adjust(self) -> None:
        self.adjusted = self.adjusted._replace(
            authors=[self.adjust_author(author) for author in self.adjusted.authors]
        )

        title = self.adjusted.title
        subtitle = self.adjusted.subtitle

        if subtitle is None:
            title, subtitle = split_title(title)

        self.update(
            title=title,
            subtitle=subtitle,
            language=normalize_language_name(self.adjusted.language),
            isbn=isbn.format(self.adjusted.isbn) if self.adjusted.isbn else None,
            issn=issn.format(self.adjusted.issn) if self.adjusted.issn else None
        )

        self.adjust_entry_date()


def adjust_entry(entry: BibEntry, logger: 'loguru.Logger') -> BibEntry:
    adjuster = BibEntryAdjuster(entry, logger)
    adjuster.adjust()
    return adjuster.adjusted


def read_entries(src: TextIO) -> Sequence[BibEntry]:
    try:
        return parse_bibtex(src.read())
    except ParsingError as err:
        raise BibToolsParsingError(str(err) + '\n\n' + err.__notes__[0]) from err


def write_entries(entries: Sequence[BibEntry], dest: TextIO) -> None:
    for i, entry in enumerate(entries):
        dest.write(str(entry))

        if i + 1 < len(entries):
            dest.write('\n')
