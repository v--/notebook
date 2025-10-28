from collections.abc import Iterable

from ..iteration import string_accumulator


@string_accumulator('')
def normalize_whitespace(string: str) -> Iterable[str]:
    whitespace_run = 0
    yielded = 0

    for char in string:
        match char:
            case '\n' | '\t' | ' ':
                whitespace_run += 1

            case _:
                if whitespace_run > 0:
                    whitespace_run = 0

                    if yielded > 0:
                        yield ' '

                yield char
                yielded += 1
