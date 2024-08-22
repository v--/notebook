from collections.abc import Sequence
from typing import NamedTuple

from ...parsing.identifiers import LatinIdentifier


class Variable(NamedTuple):
    identifier: LatinIdentifier

    def __str__(self) -> str:
        return str(self.identifier)


class FunctionTerm(NamedTuple):
    name: str
    arguments: 'Sequence[Term]'

    def __str__(self) -> str:
        args = ', '.join(str(arg) for arg in self.arguments)
        return f'{self.name}({args})' if len(args) > 0 else self.name

    def __hash__(self) -> int:
        return hash(self.name) ^ hash(tuple(self.arguments))


Term = Variable | FunctionTerm
