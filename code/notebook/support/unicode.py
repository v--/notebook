import unicodedata
from collections.abc import Iterable
from enum import Flag, auto

from .iteration import string_accumulator


class Capitalization(Flag):
    lower = auto()
    upper = auto()
    mixed = upper | lower


# The superscripts do not have adjacent codes, so we resort to using a table
SUPERSCRIPT_TABLE = str.maketrans({
    'a': 'ᵃ',
    'b': 'ᵇ',
    'c': 'ᶜ',
    'd': 'ᵈ',
    'e': 'ᵉ',
    'f': 'ᶠ',
    'g': 'ᵍ',
    'h': 'ʰ',
    'i': 'ⁱ',
    'j': 'ʲ',
    'k': 'ᵏ',
    'l': 'ˡ',
    'm': 'ᵐ',
    'n': 'ⁿ',
    'o': 'ᵒ',
    'p': 'ᵖ',
    'q': '𐞥',
    'r': 'ʳ',
    's': 'ˢ',
    't': 'ᵗ',
    'u': 'ᵘ',
    'v': 'ᵛ',
    'w': 'ʷ',
    'x': 'ˣ',
    'y': 'ʸ',
    'z': 'ᶻ',
    'A': 'ᴬ',
    'B': 'ᴮ',
    'C': 'ꟲ',
    'D': 'ᴰ',
    'E': 'ᴱ',
    'F': 'ꟳ',
    'G': 'ᴳ',
    'H': 'ᴴ',
    'I': 'ᴵ',
    'J': 'ᴶ',
    'K': 'ᴷ',
    'L': 'ᴸ',
    'M': 'ᴹ',
    'N': 'ᴺ',
    'O': 'ᴼ',
    'P': 'ᴾ',
    'Q': 'ꟴ',
    'R': 'ᴿ',
    'S': '꟱',
    'T': 'ᵀ',
    'U': 'ᵁ',
    'V': 'ⱽ',
    'W': 'ᵂ',
    '0': '⁰',
    '1': '¹',
    '2': '²',
    '3': '³',
    '4': '⁴',
    '5': '⁵',
    '6': '⁶',
    '7': '⁷',
    '8': '⁸',
    '9': '⁹'
})

SUBSCRIPT_TABLE = str.maketrans({
    'a': 'ₐ',
    'e': 'ₑ',
    'h': 'ₕ',
    'i': 'ᵢ',
    'j': 'ⱼ',
    'k': 'ₖ',
    'l': 'ₗ',
    'm': 'ₘ',
    'n': 'ₙ',
    'o': 'ₒ',
    'p': 'ₚ',
    'r': 'ᵣ',
    's': 'ₛ',
    't': 'ₜ',
    'u': 'ᵤ',
    'v': 'ᵥ',
    'x': 'ₓ',
    '0': '₀',
    '1': '₁',
    '2': '₂',
    '3': '₃',
    '4': '₄',
    '5': '₅',
    '6': '₆',
    '7': '₇',
    '8': '₈',
    '9': '₉',
})


def to_superscript(string: str) -> str:
    return string.translate(SUPERSCRIPT_TABLE)


def to_subscript(string: str) -> str:
    return string.translate(SUBSCRIPT_TABLE)


def is_numeric_subscript(string: str) -> bool:
    return '₀' <= string <= '₉'


def atoi_subscripts(string: str) -> int:
    if string[0] == '₋':
        return -atoi_subscripts(string[1:])

    assert all(map(is_numeric_subscript, string))
    return sum(
        unicodedata.digit(digit) * (10 ** i)
        for i, digit in enumerate(reversed(string))
    )


def itoa_subscripts(value: int) -> str:
    if value < 0:
        return '₋' + itoa_subscripts(-value)

    return to_subscript(str(value))


def is_latin_string(string: str, capitalization: Capitalization) -> bool:
    return all(
        ('A' <= c <= 'Z' if Capitalization.upper in capitalization else False) or
        ('a' <= c <= 'z' if Capitalization.lower in capitalization else False)
        for c in string
    )


def is_greek_string(string: str, capitalization: Capitalization) -> bool:
    return all(
        ('Α' <= c <= 'Ω' if Capitalization.upper in capitalization else False) or
        ('α' <= c <= 'ω' if Capitalization.lower in capitalization else False)
        for c in string
    )


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
def remove_whitespace(string: str) -> Iterable[str]:
    for char in string:
        match char:
            case '\n' | '\t' | ' ':
                pass

            case _:
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
