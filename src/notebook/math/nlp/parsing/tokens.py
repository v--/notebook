from typing import TYPE_CHECKING, Literal, get_args

from ....parsing import Token


if TYPE_CHECKING:
    from collections.abc import Sequence


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
