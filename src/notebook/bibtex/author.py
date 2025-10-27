from dataclasses import dataclass

from .string import BibString


@dataclass(frozen=True)
class BibAuthor:
    full_name: BibString
    short_name: BibString | None = None
