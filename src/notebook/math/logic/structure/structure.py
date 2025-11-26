from collections.abc import Collection
from typing import Protocol

from ..signature import FormalLogicSignature, SignatureSymbol


class FormalLogicStructure[T](Protocol):
    universe: Collection[T]
    signature: FormalLogicSignature

    def apply_function(self, f: SignatureSymbol, *args: T) -> T:
        ...

    def apply_predicate(self, p: SignatureSymbol, *args: T) -> bool:
        ...
