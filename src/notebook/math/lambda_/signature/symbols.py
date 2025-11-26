from dataclasses import dataclass


@dataclass(frozen=True)
class BaseSignatureSymbol:
    name: str


class ConstantTermSymbol(BaseSignatureSymbol):
    def __str__(self) -> str:
        return f'constant symbol {self.name!r}'


class BaseTypeSymbol(BaseSignatureSymbol):
    def __str__(self) -> str:
        return f'base type symbol {self.name!r}'


SignatureSymbol = ConstantTermSymbol | BaseTypeSymbol
