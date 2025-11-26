from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class BaseSignatureSymbol:
    name: str

    def __str__(self) -> str:
        return self.name


class ConstantTermSymbol(BaseSignatureSymbol):
    pass


class BaseTypeSymbol(BaseSignatureSymbol):
    pass


SignatureSymbol = ConstantTermSymbol | BaseTypeSymbol


def get_symbol_kind(sym: SignatureSymbol) -> Literal['constant term', 'base type']:
    match sym:
        case ConstantTermSymbol():
            return 'constant term'

        case BaseTypeSymbol():
            return 'base type'
