from ...structure import FormalLogicStructure
from .signature import BOOLEAN_ALGEBRA_SIGNATURE


class TwoElementBooleanAlgebra(FormalLogicStructure[bool]):
    def __init__(self) -> None:
        self.universe = { True, False }
        self.signature = BOOLEAN_ALGEBRA_SIGNATURE
        self.interpretation = {
            BOOLEAN_ALGEBRA_SIGNATURE['⫪']: lambda: True,
            BOOLEAN_ALGEBRA_SIGNATURE['⫫']: lambda: False,
            BOOLEAN_ALGEBRA_SIGNATURE['⫬']: lambda x: not x,
            BOOLEAN_ALGEBRA_SIGNATURE['⩓']: lambda x, y: x and y,
            BOOLEAN_ALGEBRA_SIGNATURE['⩔']: lambda x, y: x or y,
            BOOLEAN_ALGEBRA_SIGNATURE['≤']: lambda x, y: x <= y,
            BOOLEAN_ALGEBRA_SIGNATURE['≥']: lambda x, y: x >= y
        }
