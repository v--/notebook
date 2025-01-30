from typing import NamedTuple

from ....parsing.identifiers import GreekIdentifier, LatinIdentifier
from .terms import FunctionLikeTerm


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


class StarredTermSchema(NamedTuple):
    term: TermSchema

    def __str__(self) -> str:
        return f'{self.term}*'


ExtendedTermSchema = TermSchema | StarredTermSchema
