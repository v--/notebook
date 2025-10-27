from collections.abc import Mapping, Sequence
from typing import Literal, get_args

from ...parsing import Token, map_of_str_enum_to_tokens
from ..nodes import SpecialNode


LaTeXTokenKind = Literal[
    # Value-dependent
    'TEXT',
    'WHITESPACE',

    # Singletons
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


TOKEN_KIND_LIST: Sequence[LaTeXTokenKind] = get_args(LaTeXTokenKind)
SINGLETON_TOKEN_MAP: Mapping[str, LaTeXTokenKind] = {
    **map_of_str_enum_to_tokens(TOKEN_KIND_LIST, SpecialNode),
    '{': 'OPENING_BRACE',
    '}': 'CLOSING_BRACE',
    '[': 'OPENING_BRACKET',
    ']': 'CLOSING_BRACKET',
    '\\': 'BACKSLASH',
}


LaTeXToken = Token[LaTeXTokenKind]
