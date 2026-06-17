from typing import TextIO
lazy from collections.abc import Sequence

from notebook.bibtex import BibEntry, parse_bibtex
from notebook.parsing.parser import ParserError

from .exceptions import BibToolsParsingError


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
