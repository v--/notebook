from typing import TYPE_CHECKING, Literal

from ...parsing import StringContainer
from ...support.name_collision import get_name_without_collision


if TYPE_CHECKING:
    from collections.abc import Collection


class Terminal(StringContainer):
    def __str__(self) -> str:
        return f'"{self.value}"'

    def __repr__(self) -> str:
        return f'Terminal({self.value!r})'


class NonTerminal(StringContainer):
    def __str__(self) -> str:
        return f'<{self.value}>'

    def __repr__(self) -> str:
        return f'NonTerminal({self.value!r})'


def new_non_terminal(base: NonTerminal | Terminal | str, context: Collection[NonTerminal]) -> NonTerminal:
    return NonTerminal(
        get_name_without_collision(
            base if isinstance(base, str) else base.value,
            {sym.value for sym in context},
        ),
    )


Empty = Literal['ε']
empty: Empty = 'ε'
