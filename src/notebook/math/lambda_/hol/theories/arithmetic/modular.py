# ruff: noqa: FURB118

from notebook.math.lambda_.hol.alphabet import SortName
from notebook.math.lambda_.hol.structure import HolStructure
from notebook.math.rings.modular import BaseIntModulo

from .signature import ARITHMETIC_SIGNATURE


class ModularArithmeticStructure[T: BaseIntModulo](HolStructure[T]):
    ring: type[T]

    def __init__(self, ring: type[T]) -> None:
        self.ring = ring
        self.signature = ARITHMETIC_SIGNATURE
        self.sort_universes = {
            ARITHMETIC_SIGNATURE.get_sort_symbol(SortName.INDIVIDUAL): {ring(n) for n in range(ring.modulus)},
        }

        self.interpretation = {
            ARITHMETIC_SIGNATURE.get_nonlogical_constant_symbol('0'): self.ring(0),
            ARITHMETIC_SIGNATURE.get_nonlogical_constant_symbol('S⁺'): lambda a: a + 1,
            ARITHMETIC_SIGNATURE.get_nonlogical_constant_symbol('~'): lambda a: -a,
            ARITHMETIC_SIGNATURE.get_nonlogical_constant_symbol('+'): lambda a: (lambda b: a + b),
            ARITHMETIC_SIGNATURE.get_nonlogical_constant_symbol('×'): lambda a: (lambda b: a * b),
            ARITHMETIC_SIGNATURE.get_nonlogical_constant_symbol('≤'): lambda a: (lambda b: a <= b),
        }
