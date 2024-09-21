from collections.abc import Iterable
from typing import NamedTuple

from ..support.iteration import string_accumulator


class BibAuthor(NamedTuple):
    main_name: str
    other_names: str | None = None
    title: str | None = None
    display_name: str | None = None
    verbatim: bool = False

    @string_accumulator(' ')
    def get_shortened_string(self) -> Iterable[str]:
        if self.other_names:
            yield self.other_names.split()[0]
            yield self.main_name
        else:
            yield self.main_name

    @string_accumulator(', ')
    def get_full_string(self) -> Iterable[str]:
        yield self.main_name

        if self.title:
            yield self.title

        if self.other_names:
            yield self.other_names

    def __str__(self) -> str:
        return self.get_full_string()
