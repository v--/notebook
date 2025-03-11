from typing import Literal, get_args

from ...parsing.tokens import Token


LaTeXTokenKind = Literal[
    'TEXT',
    'WHITESPACE',

    'AT',
    'CARET',
    'PERCENT',
    'AMPERSAND',
    'UNDERSCORE',
    'DOLLAR',
    'OPENING_BRACE',
    'CLOSING_BRACE',
    'OPENING_BRACKET',
    'CLOSING_BRACKET',
    'BACKSLASH',
    'LINE_BREAK',
]


TOKEN_KIND_LIST = get_args(LaTeXTokenKind)
SINGLETON_TOKEN_MAP: dict[str, LaTeXTokenKind] = {
    '@': 'AT',
    '^': 'CARET',
    '%': 'PERCENT',
    '&': 'AMPERSAND',
    '_': 'UNDERSCORE',
    '$': 'DOLLAR',
    '{': 'OPENING_BRACE',
    '}': 'CLOSING_BRACE',
    '[': 'OPENING_BRACKET',
    ']': 'CLOSING_BRACKET',
    '\\': 'BACKSLASH',
    '\n': 'LINE_BREAK',
}


LaTeXToken = Token[LaTeXTokenKind]
