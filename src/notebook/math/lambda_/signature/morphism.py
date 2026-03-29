from dataclasses import dataclass
from typing import TYPE_CHECKING, overload

from .exceptions import MissingSignatureSymbolError, SignatureMorphismError
from .signature import LambdaSignature
from .symbols import BaseTypeSymbol, ConstantTermSymbol, SignatureSymbol


if TYPE_CHECKING:
    from collections.abc import Mapping


@dataclass
class SignatureMorphism:
    source: LambdaSignature
    mapping: Mapping[SignatureSymbol, SignatureSymbol]

    def __post_init__(self) -> None:
        for a, b in self.mapping.items():
            if a not in self.source:
                raise MissingSignatureSymbolError(f'Unrecognized {a}')

            if (isinstance(a, BaseTypeSymbol) and isinstance(b, ConstantTermSymbol)) or (isinstance(a, ConstantTermSymbol) and isinstance(b, BaseTypeSymbol)):
                raise SignatureMorphismError(f'Mismatch between the {a.get_kind_string()} symbol {a} and the {b.get_kind_string()} symbol {b}')

    @overload
    def __call__(self, symbol: BaseTypeSymbol) -> BaseTypeSymbol: ...
    @overload
    def __call__(self, symbol: ConstantTermSymbol) -> ConstantTermSymbol: ...
    @overload
    def __call__(self, symbol: SignatureSymbol) -> SignatureSymbol: ...
    def __call__(self, symbol: SignatureSymbol) -> SignatureSymbol:
        if symbol in self.mapping:
            return self.mapping[symbol]

        if symbol in self.source:
            return symbol

        raise MissingSignatureSymbolError(f'The {symbol.get_kind_string()} symbol {symbol} is not present in the source signature')

    def get_modified_signature(self) -> LambdaSignature:
        return LambdaSignature(*(self(sym) for sym in self.source))
