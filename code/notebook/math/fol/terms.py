from collections.abc import Sequence
from typing import NamedTuple

from ...parsing.identifiers import GreekIdentifier, LatinIdentifier


class Variable(NamedTuple):
    identifier: LatinIdentifier

    def __str__(self) -> str:
        return str(self.identifier)


class FunctionLikeTerm[ArgT](NamedTuple):
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


class VariablePlaceholder(NamedTuple):
    identifier: LatinIdentifier

    def __str__(self) -> str:
        return str(self.identifier)


class TermPlaceholder(NamedTuple):
    identifier: GreekIdentifier

    def __str__(self) -> str:
        return str(self.identifier)


class FunctionTermSchema(FunctionLikeTerm['TermSchema']):
    pass


TermSchema = VariablePlaceholder | TermPlaceholder | FunctionTermSchema
