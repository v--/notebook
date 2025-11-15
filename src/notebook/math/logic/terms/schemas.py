from dataclasses import dataclass

from ....parsing.identifiers import GreekIdentifier, LatinIdentifier
from .terms import FunctionLike


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


class FunctionTermSchema(FunctionLike['TermSchema']):
    pass


TermSchema = VariablePlaceholder | TermPlaceholder | FunctionTermSchema
