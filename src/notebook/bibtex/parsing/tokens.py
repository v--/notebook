from collections.abc import Mapping, Sequence
from typing import Literal, get_args

from ...parsing import Token


BibTokenKind = Literal[
    # Value-dependent
    'WORD',
    'DECIMAL',
    'SYMBOL',

    # Singletons
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


TOKEN_KIND_LIST: Sequence[BibTokenKind] = get_args(BibTokenKind)
SINGLETON_TOKEN_MAP: Mapping[str, BibTokenKind] = {
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
