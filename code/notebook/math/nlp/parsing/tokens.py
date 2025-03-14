from collections.abc import Sequence
from typing import Literal, get_args

from ....parsing import Token


TextTokenKind = Literal[
    # Value-dependent
    'WORD',
    'DECIMAL',
    'SYMBOL',
    'WHITESPACE',

    # Singletons
    'LINE_BREAK',
]


TOKEN_KIND_LIST: Sequence[TextTokenKind] = get_args(TextTokenKind)


TextToken = Token[TextTokenKind]
