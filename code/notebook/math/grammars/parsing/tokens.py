from collections.abc import Mapping, Sequence
from typing import Literal, get_args

from ....parsing import Token


GrammarTokenKind = Literal[
    # Value-dependent
    'TEXT',

    # Singletons
    'OPENING_CHEVRON',
    'CLOSING_CHEVRON',
    'DOUBLE_QUOTES',
    'RIGHT_ARROW',
    'EPSILON',
    'PIPE',
    'BACKSLASH',
    'SPACE',
    'LINE_BREAK',
]


TOKEN_KIND_LIST: Sequence[GrammarTokenKind] = get_args(GrammarTokenKind)
SINGLETON_TOKEN_MAP: Mapping[str, GrammarTokenKind] = {
    '<': 'OPENING_CHEVRON',
    '>': 'CLOSING_CHEVRON',
    '"': 'DOUBLE_QUOTES',
    '→': 'RIGHT_ARROW',
    'ε': 'EPSILON',
    '|': 'PIPE',
    '\\': 'BACKSLASH',
    ' ': 'SPACE',
    '\n': 'LINE_BREAK',
}


GrammarToken = Token[GrammarTokenKind]
