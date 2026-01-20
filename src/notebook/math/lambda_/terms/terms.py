from dataclasses import dataclass

from ....parsing.identifiers import LatinIdentifier
from ..alphabet import BinderSymbol
from ..signature import ConstantTermSymbol
from ..types import SimpleType


@dataclass(frozen=True)
class Constant:
    value: ConstantTermSymbol

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"parse_term('{self}')"


@dataclass(frozen=True)
class Variable:
    identifier: LatinIdentifier

    def __str__(self) -> str:
        return str(self.identifier)

    def __repr__(self) -> str:
        return f"parse_term('{self}')"


@dataclass(frozen=True)
class UntypedApplication:
    left: UntypedTerm
    right: UntypedTerm

    def __str__(self) -> str:
        return f'({self.left}{self.right})'

    def __repr__(self) -> str:
        return f"parse_term('{self}')"


@dataclass(frozen=True)
class TypedApplication:
    left: TypedTerm
    right: TypedTerm

    def __str__(self) -> str:
        return f'({self.left}{self.right})'

    def __repr__(self) -> str:
        return f"parse_term('{self}')"


@dataclass(frozen=True)
class UntypedAbstraction:
    var: Variable
    body: UntypedTerm

    def __str__(self) -> str:
        return f'({BinderSymbol.LAMBDA}{self.var}.{self.body})'

    def __repr__(self) -> str:
        return f"parse_term('{self}')"


@dataclass(frozen=True)
class TypedAbstraction:
    var: Variable
    var_type: SimpleType
    body: TypedTerm

    def __str__(self) -> str:
        return f'({BinderSymbol.LAMBDA}{self.var}:{self.var_type}.{self.body})'

    def __repr__(self) -> str:
        return f"parse_term('{self}')"


UntypedTerm = Constant | Variable | UntypedApplication | UntypedAbstraction
TypedTerm = Constant | Variable | TypedApplication | TypedAbstraction
