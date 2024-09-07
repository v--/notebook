from typing import TextIO

from titlecase import titlecase

from notebook.bibtex.author import BibAuthor
from notebook.bibtex.entry import BibEntry
from notebook.bibtex.parsing import parse_bibtex
from notebook.parsing.parser import ParsingError

from ..common.formatting import Formatter
from ..common.names import latinize_cyrillic_name


def titlecase_bib_callback(string: str, all_caps: bool) -> str | None:  # noqa: FBT001
    if all_caps or not string.isascii():
        return string

    return None


class BibFormatter(Formatter):
    def adjust_author(self, author: BibAuthor, entry: BibEntry) -> BibAuthor:
        adjusted = author

        if adjusted.display_name is None and (entry.language == 'russian' or entry.language == 'bulgarian'):
            adjusted = adjusted._replace(display_name=latinize_cyrillic_name(adjusted.get_shortened_string()))

        return adjusted

    def adjust_entry(self, entry: BibEntry) -> BibEntry:
        adjusted = entry
        adjusted._replace(authors=[self.adjust_author(author, adjusted) for author in adjusted.authors])

        if adjusted.entry_type == 'online':
            return adjusted

        title = titlecase(adjusted.title, callback=titlecase_bib_callback)

        if title != adjusted.title:
            self.logger.info(f'Capitalizing title {adjusted.title!r} to {title!r}')
            adjusted = adjusted._replace(title=title)

        if adjusted.subtitle:
            subtitle = titlecase(adjusted.subtitle, callback=titlecase_bib_callback)

            if subtitle != adjusted.subtitle:
                self.logger.info(f'Capitalizing subtitle {adjusted.subtitle!r} to {subtitle!r}')
                adjusted = adjusted._replace(subtitle=subtitle)

        return adjusted

    def format(self, src: TextIO, dest: TextIO) -> None:
        try:
            entries = parse_bibtex(src.read())
        except ParsingError as err:
            raise SystemExit(str(err) + '\n\n' + err.__notes__[0]) from err

        for i, entry in enumerate(entries):
            adjusted = self.adjust_entry(entry)
            dest.write(str(adjusted))

            if i + 1 < len(entries):
                dest.write('\n')
