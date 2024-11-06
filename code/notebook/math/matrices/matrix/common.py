from ...rings.types import IField, INormedField, IRing, ISemiring
from .base import BaseMatrix, MatrixDivisionMixin, MatrixSubtractionMixin
from .constructor import MatrixConstructorMixin


class ISemiringMatrix[N: ISemiring](MatrixConstructorMixin[N], BaseMatrix[N]):
    pass


class IRingMatrix[N: IRing](MatrixSubtractionMixin[N], ISemiringMatrix[N]):
    pass


class IFieldMatrix[N: IField](MatrixDivisionMixin[N], IRingMatrix[N]):
    pass


class INormedFieldMatrix[N: INormedField](IFieldMatrix[N]):
    pass
