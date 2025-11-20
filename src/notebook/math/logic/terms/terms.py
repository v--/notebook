from collections.abc import Sequence
from dataclasses import dataclass

from ....parsing.identifiers import LatinIdentifier


@dataclass(frozen=True)
class Variable:
    identifier: LatinIdentifier

    def __str__(self) -> str:
        return str(self.identifier)


@dataclass(frozen=True)
class SyntacticApplication[ArgT]:
    name: str
    arguments: Sequence[ArgT]

    def __str__(self) -> str:
        if len(self.arguments) == 0:
            return self.name

        args = ', '.join(str(arg) for arg in self.arguments)
        return f'{self.name}({args})'

    def __hash__(self) -> int:
        return hash(self.name) ^ hash(tuple(self.arguments))


class FunctionApplication(SyntacticApplication['Term']):
    pass


Term = Variable | FunctionApplication
