from typing import Literal

from ...parsing.tokens import Token


BibTokenKind = Literal[
    'WORD',
    'NUMBER',
    'SYMBOL',
    'SPACE',

    'AT',
    'PERCENT',
    'AMPERSAND',
    'OPENING_BRACE',
    'CLOSING_BRACE',
    'DOUBLE_QUOTES',
    'EQUALS',
    'COMMA',
    'UNDERSCORE',
    'BACKSLASH',
    'LINE_BREAK',
    'TAB',
]


bib_token_map: dict[str, BibTokenKind] = {
    '@': 'AT',
    '%': 'PERCENT',
    '&': 'AMPERSAND',
    '{': 'OPENING_BRACE',
    '}': 'CLOSING_BRACE',
    '"': 'DOUBLE_QUOTES',
    '=': 'EQUALS',
    ',': 'COMMA',
    '_': 'UNDERSCORE',
    '\\': 'BACKSLASH',
    '\n': 'LINE_BREAK',
    '\t': 'TAB',
}


BibToken = Token[BibTokenKind]
