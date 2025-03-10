from typing import Literal, get_args

from ....parsing.tokens import Token


TextTokenKind = Literal[
    'WORD',
    'DECIMAL',
    'SYMBOL',
    'WHITESPACE',
    'LINE_BREAK',
]


TOKEN_KIND_LIST = get_args(TextTokenKind)


TextToken = Token[TextTokenKind]
