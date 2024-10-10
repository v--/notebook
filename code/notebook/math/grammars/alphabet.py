import itertools
from collections.abc import Collection
from typing import Literal

from ...exceptions import UnreachableException
from ...parsing.tokens import TokenMixin
from ...support.unicode import atoi_subscripts, is_numeric_subscript, itoa_subscripts


class Terminal(TokenMixin):
    def __str__(self) -> str:
        return f'"{self.value}"'

    def __repr__(self) -> str:
        return f"Terminal({self.value!r})"


class NonTerminal(TokenMixin):
    def __str__(self) -> str:
        return f'<{self.value}>'

    def __repr__(self) -> str:
        return f"NonTerminal({self.value!r})"


def new_non_terminal(base_name: str, context: Collection[NonTerminal]) -> NonTerminal:
    numeric_subscript = ''.join(itertools.takewhile(is_numeric_subscript, reversed(base_name)))
    index: int = -1

    if len(numeric_subscript) > 0:
        index = atoi_subscripts(numeric_subscript)

    name_base = base_name[:len(base_name) - len(numeric_subscript)]

    for i in itertools.count(start=index + 1):
        candidate = NonTerminal(name_base + itoa_subscripts(i))

        if candidate not in context:
            return candidate

    raise UnreachableException


Empty = Literal['ε']
empty: Empty = 'ε'
