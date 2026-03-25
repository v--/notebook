from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .string import BibString


@dataclass(frozen=True)
class BibAuthor:
    full_name: BibString
    short_name: BibString | None = None
