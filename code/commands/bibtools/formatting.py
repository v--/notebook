from collections.abc import Sequence
from dataclasses import replace
from typing import Any, TextIO

import loguru
from stdnum import isbn, issn

from notebook.bibtex.author import BibAuthor
from notebook.bibtex.entry import BibEntry
from notebook.bibtex.parsing import parse_bibtex
from notebook.bibtex.string import BibString
from notebook.parsing.parser import ParserError

from ..common.names import latinize_cyrillic_name
from . import url_templates
from .exceptions import BibToolsParsingError
from .sources.common.dates import extract_year
from .sources.common.entries import regenerate_entry_name
from .sources.common.languages import get_main_entry_language, normalize_language_name
from .sources.common.names import get_main_human_name, normalize_human_name
from .sources.common.pages import normalize_pages
from .sources.common.url_template import UrlTemplate


class BibEntryAdjuster:
    original: BibEntry
    adjusted: BibEntry
    logger: 'loguru.Logger'

    def __init__(self, entry: BibEntry, logger: 'loguru.Logger') -> None:
        self.original = entry
        self.adjusted = replace(entry)
        self.logger = logger

    def log_update[T](self, what: str, old_value: T, new_value: T) -> None:
        if new_value == old_value:
            return

        if new_value is None:
            self.logger.info(f'Removing {what}')
        elif old_value is None:
            self.logger.info(f'Setting {what} to {new_value!r}')
        else:
            self.logger.info(f'Updating {what} from {old_value!r} to {new_value!r}')

    def update(self, **kwargs: Any) -> None:  # noqa: ANN401
        for field_name, new_value in kwargs.items():
            old_value = getattr(self.adjusted, field_name)

            if old_value != new_value:
                self.log_update(f'the {field_name} field', old_value, new_value)
                setattr(self.adjusted, field_name, new_value)

    def get_author_short_name(self, author: BibAuthor) -> BibString | None:
        main_language = get_main_entry_language(self.adjusted)

        if (
            author.short_name is None and \
            author.full_name != 'others' and \
            (main_language == 'russian' or main_language == 'bulgarian')
        ):
            main_name = get_main_human_name(author.full_name)

            if isinstance(main_name, str):
                return latinize_cyrillic_name(main_name)

        return author.short_name

    def adjust_author(self, author: BibAuthor) -> BibAuthor:
        full_name = author.full_name

        if isinstance(full_name, str):
            full_name = normalize_human_name(full_name)

        short_name = self.get_author_short_name(author)
        return BibAuthor(full_name=full_name, short_name=short_name)

    def adjust_language(self, language: BibString) -> BibString:
        normalized = normalize_language_name(language)
        return normalized

    def adjust_entry_date(self) -> None:
        if self.adjusted.date:
            year = extract_year(str(self.adjusted.date))

            if year is None:
                self.logger.warning(f'Could not extract year from {self.adjusted.date}')

            if self.adjusted.year:
                self.logger.warning(f'Excess year tag {self.adjusted.year} in the presence of the date tag {self.adjusted.date}')

            if self.adjusted.month:
                self.logger.warning(f'Excess month tag {self.adjusted.month} in the presence of the date tag {self.adjusted.date}')

            if self.adjusted.day:
                self.logger.warning(f'Excess day tag {self.adjusted.day} in the presence of the date tag {self.adjusted.date}')

            return

        if self.adjusted.year is None:
            if self.adjusted.urldate is None and self.adjusted.entry_type != 'mvcollection':
                self.logger.warning('The date field is blank')

            return

        date = str(self.adjusted.year)

        if isinstance(self.adjusted.month, str):
            date += '-' + self.adjusted.month.rjust(2, '0')

        if isinstance(self.adjusted.day, str):
            date += '-' + self.adjusted.day.rjust(2, '0')

        self.update(date=date, year=None, month=None, day=None)

    def check_missing_fields(self) -> None:
        possibly_reprinted = self.adjusted.pubstate is not None or self.adjusted.relatedtype == 'origpubas' or self.adjusted.relatedtype == 'origpubin' or self.adjusted.origpublisher is not None

        match self.adjusted.entry_type:
            case 'inbook' | 'incollection' | 'inproceedincs' if not self.adjusted.booktitle:
                self.logger.warning(f'No book title specified for entry type {self.adjusted.entry_type!r}')

            case 'book' | 'article' if not self.adjusted.publisher and not possibly_reprinted:
                self.logger.warning(f'No publisher and no original publication specified for entry type {self.adjusted.entry_type!r}')

            case 'article' if not self.adjusted.journal and not possibly_reprinted:
                self.logger.warning(f'No journal and no original publication specified for entry type {self.adjusted.entry_type!r}')

            case 'online' if not self.adjusted.urldate:
                self.logger.warning(f'No URL date specified for entry type {self.adjusted.entry_type!r}')

        if self.adjusted.relatedtype == 'translationof' and len(self.adjusted.origlanguages) > 0:
            self.logger.warning('Specified both an original publication and an original language')

        if len(self.adjusted.translators) > 0 and self.adjusted.relatedtype != 'translationof' and len(self.adjusted.origlanguages) == 0:
            self.logger.warning('Specified the translators, but not the original publication nor the original language')

        if len(self.adjusted.origlanguages) > 0 and len(self.adjusted.translators) == 0:
            self.logger.warning('Specified the original language, but not the translators')


    def adjust_entry_name(self) -> None:
        name = self.adjusted.entry_name

        # We assume that such entries are special, e.g. standards
        if ':' in name:
            return

        name_year = extract_year(name)
        date_year = extract_year(str(self.adjusted.date))

        if name_year and date_year and name_year != date_year:
            self.logger.info('Year mismatch between the entry name and date; using the year from the date')
            self.update(entry_name=self.adjusted.entry_name.replace(name_year, date_year))

        if self.adjusted.entry_type.startswith('mv'):
            return

        if name_year is None:
            self.logger.warning('No year present in the entry name')
        elif name.endswith(name_year):
            self.logger.warning('No subject present in the entry name')
        else:
            return

        suggestion = regenerate_entry_name(self.adjusted, get_main_entry_language(self.adjusted))
        self.logger.warning(f'Consider the entry name {suggestion}')

    def adjust_url_identifier(self, field_name: str, url_template: UrlTemplate | None = None) -> None:
        if url_template is None:
            url_template = getattr(url_templates, field_name)

        if identifier := getattr(self.adjusted, field_name):
            # This is in case the URL is recorded rather than the ID
            if url_data := url_template.extract(identifier):
                self.update(**{field_name: url_data['identifier']})

            if isinstance(self.adjusted.url, str) and url_templates.clean_identifier(self.adjusted.url, url_template) == identifier:
                self.logger.info(f'Removing redundant {field_name} URL')
                self.update(url=None)
        elif isinstance(self.adjusted.url, str) and (url_data := url_template.extract(self.adjusted.url)):
            self.logger.info(f'Extracting a {field_name} identifier from the URL')
            self.update(**{field_name: url_data['identifier'], 'url': None})

    def adjust_identifiers(self) -> None:
        self.adjust_url_identifier('doi')
        self.adjust_url_identifier('eudml')
        self.adjust_url_identifier('handle')
        self.adjust_url_identifier('jstor')
        self.adjust_url_identifier('mathnet')
        self.adjust_url_identifier('mathscinet')
        self.adjust_url_identifier('numdam')
        self.adjust_url_identifier('scopus')
        self.adjust_url_identifier('ssrn')
        self.adjust_url_identifier('zbmath')

    def adjust_eprint(self) -> None:
        eprint = self.adjusted.eprint
        eprint_type = self.adjusted.eprinttype
        eprint_class = self.adjusted.eprintclass

        if not eprint_class and not eprint and not eprint_type:
            return

        if eprint_class and not eprint and not eprint_type:
            self.logger.warning(f'No eprint type or id specified for class {eprint_class!r}')
            return

        if eprint and not eprint_type:
            self.logger.warning(f'No eprint type specified for {eprint!r}')
            return

        if eprint_type and not eprint:
            self.logger.warning(f'No eprint id specified for type {eprint_type!r}')
            return

        match eprint_type:
            case 'arXiv':
                if not eprint_class:
                    self.logger.warning(f'No eprint class specified for arXiv entry {eprint!r}')

                self.adjust_url_identifier('eprint', url_templates.arxiv)

            case 'HAL':
                self.adjust_url_identifier('eprint', url_templates.hal)

    def adjust_url(self) -> None:
        url = self.adjusted.url

        if not isinstance(url, str):
            return

        match self.adjusted.eprinttype:
            case 'arXiv' if url_templates.clean_identifier(url, url_templates.arxiv) == self.adjusted.eprint:
                self.logger.info('Redundant arXiv URL')
                self.update(url=None)

            case 'HAL' if url_templates.clean_identifier(url, url_templates.hal) == self.adjusted.eprint:
                self.logger.info('Redundant HAL URL')
                self.update(url=None)

    def adjust(self) -> None:
        self.check_missing_fields()
        self.adjust_entry_name()

        if len(self.adjusted.authors) == 0 and len(self.adjusted.editors) == 0:
            self.logger.warning('Entry has neither authors nor editors specified')

        self.update(
            # authors
            authors=[self.adjust_author(author) for author in self.adjusted.authors],
            editors=[self.adjust_author(author) for author in self.adjusted.editors],
            compilers=[self.adjust_author(author) for author in self.adjusted.compilers],
            translators=[self.adjust_author(author) for author in self.adjusted.translators],
            annotators=[self.adjust_author(author) for author in self.adjusted.annotators],
            advisors=[self.adjust_author(author) for author in self.adjusted.advisors],
            # # languages
            languages=[self.adjust_language(author) for author in self.adjusted.languages],
            origlanguages=[self.adjust_language(author) for author in self.adjusted.origlanguages],
            # other
            pages=normalize_pages(self.adjusted.pages) if isinstance(self.adjusted.pages, str) else self.adjusted.pages,
            isbn=isbn.format(self.adjusted.isbn) if self.adjusted.isbn else None,
            issn=','.join(map(issn.format, self.adjusted.issn.split(','))) if isinstance(self.adjusted.issn, str) else self.adjusted.issn
        )

        if isinstance(self.adjusted.issn, str) and ',' in self.adjusted.issn:
            self.logger.warning('Multiple ISSN numbers specified')

        self.adjust_identifiers()
        self.adjust_eprint()
        self.adjust_url()
        self.adjust_entry_date()


def adjust_entry(entry: BibEntry, logger: 'loguru.Logger') -> BibEntry:
    adjuster = BibEntryAdjuster(entry, logger)
    adjuster.adjust()
    return adjuster.adjusted


def read_entries(src: TextIO) -> Sequence[BibEntry]:
    try:
        return parse_bibtex(src.read())
    except ParserError as err:
        raise BibToolsParsingError(str(err) + '\n\n' + err.__notes__[0]) from err


def write_entries(entries: Sequence[BibEntry], dest: TextIO) -> None:
    for i, entry in enumerate(entries):
        dest.write(str(entry))

        if i + 1 < len(entries):
            dest.write('\n')
