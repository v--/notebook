from dataclasses import dataclass


@dataclass(frozen=True)
class BaseSignatureSymbol:
    name: str
    arity: int
    infix: bool


class FunctionSymbol(BaseSignatureSymbol):
    def __str__(self) -> str:
        return f'function symbol {self.name!r}'


class PredicateSymbol(BaseSignatureSymbol):
    def __str__(self) -> str:
        return f'predicate symbol {self.name!r}'


SignatureSymbol = FunctionSymbol | PredicateSymbol
