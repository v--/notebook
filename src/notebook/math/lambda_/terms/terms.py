from dataclasses import dataclass

from ....parsing.identifiers import LatinIdentifier
from ..alphabet import ImproperTermSymbol
from ..types import SimpleType


@dataclass(frozen=True)
class Constant:
    name: str

    def __str__(self) -> str:
        return str(self.name)


@dataclass(frozen=True)
class Variable:
    identifier: LatinIdentifier

    def __str__(self) -> str:
        return str(self.identifier)


@dataclass(frozen=True)
class UntypedApplication:
    left: UntypedTerm
    right: UntypedTerm

    def __str__(self) -> str:
        return f'({self.left}{self.right})'


@dataclass(frozen=True)
class TypedApplication:
    left: TypedTerm
    right: TypedTerm

    def __str__(self) -> str:
        return f'({self.left}{self.right})'


@dataclass(frozen=True)
class UntypedAbstraction:
    var: Variable
    body: UntypedTerm

    def __str__(self) -> str:
        return f'({ImproperTermSymbol.LAMBDA}{self.var}.{self.body})'


@dataclass(frozen=True)
class TypedAbstraction:
    var: Variable
    var_type: SimpleType
    body: TypedTerm

    def __str__(self) -> str:
        return f'({ImproperTermSymbol.LAMBDA}{self.var}:{self.var_type}.{self.body})'


UntypedTerm = Constant | Variable | UntypedApplication | UntypedAbstraction
TypedTerm = Constant | Variable | TypedApplication | TypedAbstraction
