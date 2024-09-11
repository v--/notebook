from typing import NamedTuple

from notebook.math.nlp.parsing import tokenize_text


class Titles(NamedTuple):
    main: str
    sub: str | None


def split_title(full_title: str) -> Titles:
    titles = iter(tokenize_text(full_title).split_by(lambda token: str(token) in '.:-', limit=2))
    title = next(titles)

    try:
        subtitle = next(titles)
        return Titles(str(title), str(subtitle).lstrip('- '))
    except StopIteration:
        return Titles(str(title), None)
