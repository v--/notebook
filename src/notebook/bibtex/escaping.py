lazy from collections.abc import Iterable

from notebook.support.iteration import string_accumulator

lazy from .string import BibString


@string_accumulator('')
def escape(string: BibString) -> Iterable[str]:
    escaping = False

    for char in str(string):
        match char:
            case '\\':
                escaping = not escaping
                yield char

            case '&' | '@':
                if not escaping:
                    yield '\\'

                escaping = False
                yield char

            case _:
                escaping = False
                yield char
