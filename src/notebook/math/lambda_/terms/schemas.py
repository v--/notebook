from dataclasses import dataclass

from ....parsing.identifiers import LatinIdentifier
from ..alphabet import BinderSymbol
from ..types import SimpleTypeSchema
from .terms import Constant


@dataclass(frozen=True)
class VariablePlaceholder:
    identifier: LatinIdentifier

    def __str__(self) -> str:
        return str(self.identifier)


@dataclass(frozen=True)
class TermPlaceholder:
    identifier: LatinIdentifier

    def __str__(self) -> str:
        return str(self.identifier)


@dataclass(frozen=True)
class TypedApplicationSchema:
    left: TypedTermSchema
    right: TypedTermSchema

    def __str__(self) -> str:
        return f'({self.left}{self.right})'


@dataclass(frozen=True)
class TypedAbstractionSchema:
    var: VariablePlaceholder
    var_type: SimpleTypeSchema
    body: TypedTermSchema

    def __str__(self) -> str:
        return f'({BinderSymbol.LAMBDA}{self.var}:{self.var_type}.{self.body})'


TypedTermSchema = Constant | VariablePlaceholder | TermPlaceholder | TypedApplicationSchema | TypedAbstractionSchema
