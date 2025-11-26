from collections.abc import Sequence
from dataclasses import dataclass

from ....parsing.identifiers import LatinIdentifier
from ..exceptions import FormalLogicError
from ..signature import FunctionSymbol, SignatureSymbol


@dataclass(frozen=True)
class Variable:
    identifier: LatinIdentifier

    def __str__(self) -> str:
        return str(self.identifier)


@dataclass(frozen=True)
class SyntacticApplication[ArgT]:
    symbol: SignatureSymbol
    arguments: Sequence[ArgT]

    def __post_init__(self) -> None:
        if len(self.arguments) != self.symbol.arity:
            raise FormalLogicError(f'Unexpected argument count {len(self.arguments)} for {self.symbol.get_kind_string()} {self.symbol} with arity {self.symbol.arity}')

    def __str__(self) -> str:
        if self.symbol.arity == 0:
            return self.symbol.name

        match self.symbol.notation:
            case 'INFIX':
                [left, right] = self.arguments
                return f'({left} {self.symbol.name} {right})'

            case 'PREFIX':
                args = ', '.join(str(arg) for arg in self.arguments)
                return f'{self.symbol.name}({args})'

            case 'CONDENSED':
                args = ''.join(str(arg) for arg in self.arguments)
                return f'{self.symbol.name}{args}'

    def __hash__(self) -> int:
        return hash(self.symbol.name) ^ hash(tuple(self.arguments))


class FunctionApplication(SyntacticApplication['Term']):
    symbol: FunctionSymbol


Term = Variable | FunctionApplication
