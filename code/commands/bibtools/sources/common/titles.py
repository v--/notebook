import re
from typing import NamedTuple

from notebook.support.unicode import normalize_whitespace


class Titles(NamedTuple):
    title: str
    subtitle: str | None


def split_title(full_title: str) -> Titles:
    titles = re.split('[.:]', normalize_whitespace(full_title), maxsplit=2)

    if len(titles) == 2:
        title, subtitle = titles
        return Titles(title.strip(), subtitle.strip())

    title, = titles
    return Titles(title.strip(), None)
