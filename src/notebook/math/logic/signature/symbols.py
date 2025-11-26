from dataclasses import dataclass
from typing import Literal


SignatureSymbolNotation = Literal['PREFIX', 'INFIX', 'CONDENSED']


@dataclass(frozen=True)
class BaseSignatureSymbol:
    name: str
    arity: int
    notation: SignatureSymbolNotation = 'PREFIX'

    def __str__(self) -> str:
        return self.name


class FunctionSymbol(BaseSignatureSymbol):
    pass


class PredicateSymbol(BaseSignatureSymbol):
    pass


SignatureSymbol = FunctionSymbol | PredicateSymbol


def get_symbol_kind(sym: SignatureSymbol) -> Literal['function', 'predicate']:
    match sym:
        case FunctionSymbol():
            return 'function'

        case PredicateSymbol():
            return 'predicate'
