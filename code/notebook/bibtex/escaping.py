from collections.abc import Iterable

from ..support.iteration import string_accumulator


@string_accumulator('')
def escape(string: str) -> Iterable[str]:
    escaping = False

    for char in string:
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
