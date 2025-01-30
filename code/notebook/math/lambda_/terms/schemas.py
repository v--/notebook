from typing import NamedTuple

from ....parsing.identifiers import LatinIdentifier
from ..alphabet import TermConnective
from .terms import Constant


class VariablePlaceholder(NamedTuple):
    identifier: LatinIdentifier

    def __str__(self) -> str:
        return str(self.identifier)


class TermPlaceholder(NamedTuple):
    identifier: LatinIdentifier

    def __str__(self) -> str:
        return str(self.identifier)


class ApplicationSchema(NamedTuple):
    a: 'TermSchema'
    b: 'TermSchema'

    def __str__(self) -> str:
        return f'({self.a}{self.b})'


class AbstractionSchema(NamedTuple):
    var: VariablePlaceholder
    sub: 'TermSchema'

    def __str__(self) -> str:
        return f'({TermConnective.l}{self.var}.{self.sub})'


TermSchema = Constant | VariablePlaceholder | TermPlaceholder | ApplicationSchema | AbstractionSchema
