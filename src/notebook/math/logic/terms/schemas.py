from dataclasses import dataclass

from ....parsing.identifiers import GreekIdentifier, LatinIdentifier
from .terms import SyntacticApplication


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


class FunctionApplicationSchema(SyntacticApplication['TermSchema']):
    pass


TermSchema = VariablePlaceholder | TermPlaceholder | FunctionApplicationSchema
