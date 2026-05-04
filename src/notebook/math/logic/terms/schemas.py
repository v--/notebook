from dataclasses import dataclass
from typing import TYPE_CHECKING

from .terms import SyntacticApplication


if TYPE_CHECKING:
    from notebook.math.logic.signature import FunctionSymbol
    from notebook.parsing.identifiers import GreekIdentifier, LatinIdentifier


@dataclass(frozen=True)
class VariablePlaceholder:
    identifier: LatinIdentifier

    def __str__(self) -> str:
        return str(self.identifier)

    def __repr__(self) -> str:
        return f"parse_term_schema('{self}')"


@dataclass(frozen=True)
class TermPlaceholder:
    identifier: GreekIdentifier

    def __str__(self) -> str:
        return str(self.identifier)

    def __repr__(self) -> str:
        return f"parse_term_schema('{self}')"


class FunctionApplicationSchema(SyntacticApplication['TermSchema']):
    symbol: FunctionSymbol

    def __repr__(self) -> str:
        return f"parse_term_schema('{self}')"


TermSchema = VariablePlaceholder | TermPlaceholder | FunctionApplicationSchema
