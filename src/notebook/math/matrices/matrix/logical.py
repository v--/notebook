from ...rings.modular import Z2
from .common import IRingMatrix


class LogicalMatrix(IRingMatrix[Z2], semiring=Z2):
    pass
