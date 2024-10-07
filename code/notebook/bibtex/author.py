from typing import NamedTuple

from .string import BibString


class BibAuthor(NamedTuple):
    full_name: BibString
    short_name: BibString | None = None
