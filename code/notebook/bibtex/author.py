from typing import NamedTuple


class BibAuthor(NamedTuple):
    full_name: str
    short_name: str | None = None
    verbatim: bool = False
