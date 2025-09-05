from dataclasses import dataclass

from ....parsing.identifiers import GreekIdentifier, LatinIdentifier
from .terms import FunctionLikeTerm


@dataclass(frozen=True)
class VariablePlaceholder:
    identifier: LatinIdentifier

    def __str__(self) -> str:
        return str(self.identifier)


@dataclass(frozen=True)
class TermPlaceholder:
    identifier: GreekIdentifier

    def __str__(self) -> str:
        return str(self.identifier)


class FunctionTermSchema(FunctionLikeTerm['TermSchema']):
    pass


TermSchema = VariablePlaceholder | TermPlaceholder | FunctionTermSchema
