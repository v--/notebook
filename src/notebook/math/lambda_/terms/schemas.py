from dataclasses import dataclass
from typing import TYPE_CHECKING

from notebook.math.lambda_.alphabet import BinderSymbol

from .terms import Constant


if TYPE_CHECKING:
    from notebook.math.lambda_.types import SimpleTypeSchema
    from notebook.parsing.identifiers import LatinIdentifier


@dataclass(frozen=True)
class VariablePlaceholder:
    identifier: LatinIdentifier

    def __str__(self) -> str:
        return str(self.identifier)

    def __repr__(self) -> str:
        return f"parse_term_schema('{self}')"


@dataclass(frozen=True)
class TermPlaceholder:
    identifier: LatinIdentifier

    def __str__(self) -> str:
        return str(self.identifier)

    def __repr__(self) -> str:
        return f"parse_term_schema('{self}')"


@dataclass(frozen=True)
class TypedApplicationSchema:
    left: TypedTermSchema
    right: TypedTermSchema

    def __str__(self) -> str:
        return f'({self.left}{self.right})'

    def __repr__(self) -> str:
        return f"parse_term_schema('{self}')"


@dataclass(frozen=True)
class TypedAbstractionSchema:
    var: VariablePlaceholder
    var_type: SimpleTypeSchema
    body: TypedTermSchema

    def __str__(self) -> str:
        return f'({BinderSymbol.LAMBDA}{self.var}:{self.var_type}.{self.body})'

    def __repr__(self) -> str:
        return f"parse_term_schema('{self}')"


TypedTermSchema = Constant | VariablePlaceholder | TermPlaceholder | TypedApplicationSchema | TypedAbstractionSchema
