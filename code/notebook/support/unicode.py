import unicodedata
from typing import Iterable


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
    'W': 'ᵂ'
})


def to_superscript(string: str) -> str:
    return string.translate(SUPERSCRIPT_TABLE)


def atoi_subscripts(string: str) -> int:
    if string[0] == '₋':
        return -atoi_subscripts(string[1:])

    return sum(
        unicodedata.digit(digit) * (10 ** i)
        for i, digit in enumerate(reversed(string))
    )


def _iter_itoa_subscripts(value: int) -> Iterable[str]:
    assert value > 0

    while value > 0:
        yield chr(ord('₀') + value % 10)

        if value == 10:
            yield '₀'

        value //= 10


def itoa_subscripts(value: int) -> str:
    if value == 0:
        return '₀'

    if value < 0:
        return '₋' + itoa_subscripts(-value)

    return ''.join(reversed(list(_iter_itoa_subscripts(value))))
