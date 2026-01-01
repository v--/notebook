from collections.abc import Collection

from .....support.iteration import power_set
from ...structure import FormalLogicStructure
from .signature import BOOLEAN_ALGEBRA_SIGNATURE


class PowerSetBooleanAlgebra[T](FormalLogicStructure[Collection[T]]):
    base_set: Collection[T]

    def __init__(self, base_set: Collection[T]) -> None:
        self.base_set = base_set
        self.universe = power_set(base_set)
        self.signature = BOOLEAN_ALGEBRA_SIGNATURE
        self.interpretation = {
            BOOLEAN_ALGEBRA_SIGNATURE['⫪']: lambda: base_set,
            BOOLEAN_ALGEBRA_SIGNATURE['⫫']: lambda: set(),
            BOOLEAN_ALGEBRA_SIGNATURE['⫬']: lambda a: frozenset(x for x in base_set if x not in a),
            BOOLEAN_ALGEBRA_SIGNATURE['⩓']: lambda a, b: frozenset(x for x in base_set if x in a and x in b),
            BOOLEAN_ALGEBRA_SIGNATURE['⩔']: lambda a, b: frozenset(x for x in base_set if x in a or x in b),
            BOOLEAN_ALGEBRA_SIGNATURE['≤']: lambda a, b: all(x not in a or x in b for x in base_set),
            BOOLEAN_ALGEBRA_SIGNATURE['≥']: lambda a, b: all(x not in b or x in a for x in base_set),
        }
