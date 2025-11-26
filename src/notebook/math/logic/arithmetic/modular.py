from collections.abc import Collection

from ...rings.modular import BaseIntModulo
from ..signature import FormalLogicSignature, SignatureSymbol
from ..structure import FormalLogicStructure
from .signature import ARITHMETIC_SIGNATURE


class ModularArithmeticStructure[T: BaseIntModulo](FormalLogicStructure[T]):
    ring: type[T]
    universe: Collection[T]
    signature: FormalLogicSignature

    def __init__(self, ring: type[T]) -> None:
        self.ring = ring
        self.universe = {ring(n) for n in range(ring.modulus)}
        self.signature = ARITHMETIC_SIGNATURE

    def apply_function(self, f: SignatureSymbol, *args: T) -> T:
        match f.name:
            case '0':
                return self.ring(0)

            case '+':
                return args[0] + args[1]

            case '×':
                return args[0] * args[1]

            case _:
                raise NotImplementedError

    def apply_predicate(self, p: SignatureSymbol, *args: T) -> bool:
        match p.name:
            case '≤':
                return args[0].value <= args[1].value

            case _:
                raise NotImplementedError
