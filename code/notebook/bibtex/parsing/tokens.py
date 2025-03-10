from typing import Literal, get_args

from ...parsing.tokens import Token


BibTokenKind = Literal[
    'WORD',
    'DECIMAL',
    'SYMBOL',

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
    'SPACE',
    'TAB',
    'LINE_BREAK',
]


TOKEN_KIND_LIST = get_args(BibTokenKind)
SINGLETON_TOKEN_MAP: dict[str, BibTokenKind] = {
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
    ' ': 'SPACE',
    '\t': 'TAB',
    '\n': 'LINE_BREAK',
}


BibToken = Token[BibTokenKind]
