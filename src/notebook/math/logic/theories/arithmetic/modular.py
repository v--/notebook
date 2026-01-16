from ....rings.modular import BaseIntModulo
from ...structure import FormalLogicStructure
from .signature import ARITHMETIC_SIGNATURE


class ModularArithmeticStructure[T: BaseIntModulo](FormalLogicStructure[T]):
    ring: type[T]

    def __init__(self, ring: type[T]) -> None:
        self.ring = ring
        self.universe = {ring(n) for n in range(ring.modulus)}
        self.signature = ARITHMETIC_SIGNATURE
        self.interpretation = {
            ARITHMETIC_SIGNATURE['0']: lambda: self.ring(0),
            ARITHMETIC_SIGNATURE['S']: lambda a: a + 1,
            ARITHMETIC_SIGNATURE['~']: lambda a: -a,
            ARITHMETIC_SIGNATURE['+']: lambda a, b: a + b,
            ARITHMETIC_SIGNATURE['×']: lambda a, b: a * b,
            ARITHMETIC_SIGNATURE['≤']: lambda a, b: a <= b,
        }
