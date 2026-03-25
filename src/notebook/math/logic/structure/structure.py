from dataclasses import dataclass
from typing import TYPE_CHECKING, overload

from .exceptions import FormalLogicInterpretationError, MissingInterpretationError


if TYPE_CHECKING:
    from collections.abc import Callable, Collection, Mapping

    from ..signature import FormalLogicSignature, FunctionSymbol, PredicateSymbol, SignatureSymbol


@dataclass
class FormalLogicStructure[T]:
    signature: FormalLogicSignature
    universe: Collection[T]
    interpretation: Mapping[SignatureSymbol, Callable[..., T] | Callable[..., bool]]

    @overload
    def apply(self, sym: FunctionSymbol, *args: T) -> T: ...
    @overload
    def apply(self, sym: PredicateSymbol, *args: T) -> bool: ...
    @overload
    def apply(self, sym: SignatureSymbol, *args: T) -> T | bool: ...
    def apply(self, sym: SignatureSymbol, *args: T) -> T | bool:
        if sym not in self.interpretation:
            raise MissingInterpretationError(f'No interpretation specified for {sym}')

        if sym.arity != len(args):
            raise FormalLogicInterpretationError(f'The {sym} has arity {sym.arity}, but {len(args)} are given.')

        return self.interpretation[sym](*args)
