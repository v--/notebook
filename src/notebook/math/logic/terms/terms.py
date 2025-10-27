from collections.abc import Sequence
from dataclasses import dataclass

from ....parsing.identifiers import LatinIdentifier


@dataclass(frozen=True)
class Variable:
    identifier: LatinIdentifier

    def __str__(self) -> str:
        return str(self.identifier)


@dataclass(frozen=True)
class FunctionLikeTerm[ArgT]:
    name: str
    arguments: 'Sequence[ArgT]'

    def __str__(self) -> str:
        args = ', '.join(str(arg) for arg in self.arguments)
        return f'{self.name}({args})' if len(args) > 0 else self.name

    def __hash__(self) -> int:
        return hash(self.name) ^ hash(tuple(self.arguments))


class FunctionTerm(FunctionLikeTerm['Term']):
    pass


Term = Variable | FunctionTerm
