import re
from typing import NamedTuple

from notebook.bibtex.parsing import parse_value
from notebook.bibtex.string import BibString
from notebook.support.unicode import normalize_whitespace


class Titles(NamedTuple):
    main: BibString
    sub: BibString | None

    def __str__(self) -> str:
        if self.sub is None:
            return str(self.main)

        return f'{self.main}. {self.sub}'


def split_title(full_title: BibString) -> Titles:
    if not isinstance(full_title, str):
        return Titles(full_title, None)

    titles = re.split(r'\. |: | -+ ', full_title, maxsplit=1)

    if len(titles) == 1:
        return Titles(titles[0], None)

    return Titles(titles[0], titles[1])


def construct_titles(title: str, subtitle: str | None = None) -> Titles:
    parsed_title = parse_value(normalize_whitespace(title))
    parsed_subtitle = parse_value(normalize_whitespace(subtitle)) if subtitle else None

    if parsed_subtitle is None:
        return split_title(parsed_title)

    return Titles(
        parsed_title,
        parsed_subtitle
    )
