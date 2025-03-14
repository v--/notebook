import unicodedata
from collections.abc import Iterable

from ..iteration import string_accumulator


ACCENT_EXCEPTIONS = ['й', 'ё']
ACCENT_REPLACEMENTS = {'Ł': 'L', 'ł': 'l'}


# Based on https://stackoverflow.com/a/517974
def remove_accents_for_char(char: str) -> str:
    if char in ACCENT_REPLACEMENTS:
        return ACCENT_REPLACEMENTS[char]

    if char.lower() in ACCENT_EXCEPTIONS:
        return char

    return ''.join(c for c in unicodedata.normalize('NFKD', char) if not unicodedata.combining(c))


def remove_accents(string: str) -> str:
    return ''.join(map(remove_accents_for_char, string))


@string_accumulator('')
def remove_symbols(string: str) -> Iterable[str]:
    for char in string:
        cat = unicodedata.category(char)

        if not cat.startswith('P') and not cat.startswith('S'):
            yield char


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
