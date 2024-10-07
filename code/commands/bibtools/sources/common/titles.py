import re
from typing import NamedTuple

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


def construct_titles(title: BibString, subtitle: BibString | None = None) -> Titles:
    if not isinstance(title, str):
        return Titles(
            title,
            normalize_whitespace(subtitle) if isinstance(subtitle, str) else subtitle
        )

    if subtitle is None or subtitle == '':
        return split_title(
            normalize_whitespace(title)
        )

    return Titles(
        normalize_whitespace(title),
        normalize_whitespace(subtitle) if isinstance(subtitle, str) else subtitle
    )
