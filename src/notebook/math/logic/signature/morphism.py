from collections.abc import Mapping
from dataclasses import dataclass
from typing import overload

from .exceptions import MissingSignatureSymbolError, SignatureTranslationError
from .signature import FormalLogicSignature
from .symbols import FunctionSymbol, PredicateSymbol, SignatureSymbol


@dataclass
class SignatureMorphism:
    source: FormalLogicSignature
    mapping: Mapping[SignatureSymbol, SignatureSymbol]

    def __post_init__(self) -> None:
        for a, b in self.mapping.items():
            if a not in self.source:
                raise MissingSignatureSymbolError(f'Unrecognized {a}')

            if (isinstance(a, FunctionSymbol) and isinstance(b, PredicateSymbol)) or (isinstance(a, PredicateSymbol) and isinstance(b, FunctionSymbol)):
                raise SignatureTranslationError(f'Mismatch between the {a} and the {b}')

            if a.arity != b.arity:
                raise SignatureTranslationError(f'Mismatch between {a} of arity {a.arity} and {b} of arity {b.arity}')

    @overload
    def __call__(self, symbol: FunctionSymbol) -> FunctionSymbol: ...
    @overload
    def __call__(self, symbol: PredicateSymbol) -> PredicateSymbol: ...
    @overload
    def __call__(self, symbol: SignatureSymbol) -> SignatureSymbol: ...
    def __call__(self, symbol: SignatureSymbol) -> SignatureSymbol:
        if symbol in self.mapping:
            return self.mapping[symbol]

        if symbol not in self.source:
            return symbol

        raise MissingSignatureSymbolError(f'The {symbol} is not present in the source signature')
