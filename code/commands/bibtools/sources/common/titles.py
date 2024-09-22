import re
from typing import NamedTuple

from notebook.bibtex.verbatim import is_verbatim_string


class Titles(NamedTuple):
    main: str
    sub: str | None

    def __str__(self) -> str:
        if self.sub is None:
            return self.main

        return f'{self.main}. {self.sub}'


def split_title(full_title: str) -> Titles:
    if is_verbatim_string(full_title):
        return Titles(full_title, None)

    titles = re.split(r'\. |: | -+ ', full_title, maxsplit=1)

    if len(titles) == 1:
        return Titles(titles[0], None)

    return Titles(titles[0], titles[1])
