# ruff: noqa: FURB118

from ...rings.modular import BaseIntModulo
from ..parsing import parse_type
from .signature import HolSignature, NonLogicalConstantSymbol, common_types
from .structure import HolStructure


ARITHMETIC_SIGNATURE = HolSignature(common_types.individual)
ARITHMETIC_SIGNATURE.add_symbol(NonLogicalConstantSymbol('0'), parse_type('ι', ARITHMETIC_SIGNATURE))
ARITHMETIC_SIGNATURE.add_symbol(NonLogicalConstantSymbol('S⁺'), parse_type('(ι → ι)', ARITHMETIC_SIGNATURE))
ARITHMETIC_SIGNATURE.add_symbol(NonLogicalConstantSymbol('~'), parse_type('(ι → ι)', ARITHMETIC_SIGNATURE))
ARITHMETIC_SIGNATURE.add_symbol(NonLogicalConstantSymbol('+'), parse_type('(ι → (ι → ι))', ARITHMETIC_SIGNATURE))
ARITHMETIC_SIGNATURE.add_symbol(NonLogicalConstantSymbol('×'), parse_type('(ι → (ι → ι))', ARITHMETIC_SIGNATURE))
ARITHMETIC_SIGNATURE.add_symbol(NonLogicalConstantSymbol('≤'), parse_type('(ι → (ι → ο))', ARITHMETIC_SIGNATURE))


class ModularArithmeticStructure[T: BaseIntModulo](HolStructure[T]):
    ring: type[T]

    def __init__(self, ring: type[T]) -> None:
        self.ring = ring
        self.signature = ARITHMETIC_SIGNATURE
        self.sort_universes = {
            common_types.individual: {ring(n) for n in range(ring.modulus)},
        }

        self.interpretation = {
            ARITHMETIC_SIGNATURE.get_nonlogical_constant_symbol('0'): self.ring(0),
            ARITHMETIC_SIGNATURE.get_nonlogical_constant_symbol('S⁺'): lambda a: a + 1,
            ARITHMETIC_SIGNATURE.get_nonlogical_constant_symbol('~'): lambda a: -a,
            ARITHMETIC_SIGNATURE.get_nonlogical_constant_symbol('+'): lambda a: (lambda b: a + b),
            ARITHMETIC_SIGNATURE.get_nonlogical_constant_symbol('×'): lambda a: (lambda b: a * b),
            ARITHMETIC_SIGNATURE.get_nonlogical_constant_symbol('≤'): lambda a: (lambda b: a <= b),
        }
