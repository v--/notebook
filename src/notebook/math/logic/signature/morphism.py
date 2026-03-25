from dataclasses import dataclass
from typing import TYPE_CHECKING, overload

from .exceptions import MissingSignatureSymbolError, SignatureMorphismError
from .symbols import FunctionSymbol, PredicateSymbol, SignatureSymbol


if TYPE_CHECKING:
    from collections.abc import Mapping

    from .signature import FormalLogicSignature


@dataclass
class SignatureMorphism:
    source: FormalLogicSignature
    mapping: Mapping[SignatureSymbol, SignatureSymbol]

    def __post_init__(self) -> None:
        for a, b in self.mapping.items():
            if a not in self.source:
                raise MissingSignatureSymbolError(f'Unrecognized {a}')

            if (isinstance(a, FunctionSymbol) and isinstance(b, PredicateSymbol)) or (isinstance(a, PredicateSymbol) and isinstance(b, FunctionSymbol)):
                raise SignatureMorphismError(f'Mismatch between the {a.get_kind_string()} symbol {a} and the {b.get_kind_string()} symbol {b}')

            if a.arity != b.arity:
                raise SignatureMorphismError(f'Mismatch between the arity {a.arity} of the {a.get_kind_string()} symbol {a} and the arity {b.arity} of the {b.get_kind_string()} symbol {b}')

    @overload
    def __call__(self, symbol: FunctionSymbol) -> FunctionSymbol: ...
    @overload
    def __call__(self, symbol: PredicateSymbol) -> PredicateSymbol: ...
    @overload
    def __call__(self, symbol: SignatureSymbol) -> SignatureSymbol: ...
    def __call__(self, symbol: SignatureSymbol) -> SignatureSymbol:
        if symbol in self.mapping:
            return self.mapping[symbol]

        if symbol in self.source:
            return symbol

        raise MissingSignatureSymbolError(f'The {symbol.get_kind_string()} symbol {symbol} is not present in the source signature')
