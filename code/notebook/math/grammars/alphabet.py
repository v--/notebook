from typing import Literal

from ...parsing.tokens import TokenMixin


class Terminal(TokenMixin):
    def __str__(self):
        return f'"{self.value}"'


class NonTerminal(TokenMixin):
    def __str__(self):
        return f'<{self.value}>'


Empty = Literal['ε']
empty: Empty = 'ε'
