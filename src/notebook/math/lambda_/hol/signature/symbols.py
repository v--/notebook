from dataclasses import dataclass
from typing import TYPE_CHECKING, override

from .....support.inference import ImproperInferenceRuleSymbol
from ...alphabet import AuxImproperSymbol, BinaryTypeConnective
from ...signature import BaseTypeSymbol, ConstantTermSymbol, LambdaSignatureError


if TYPE_CHECKING:
    from ...types import SimpleType


# We allow Greek identifiers as sorts since we forbid type variables
class HolTypeSymbol(BaseTypeSymbol):
    @override
    def validate(self, name: str) -> None:
        if name in BinaryTypeConnective or name in AuxImproperSymbol or name in ImproperInferenceRuleSymbol:
            raise LambdaSignatureError(f'Cannot use the improper symbol {name} as a base type')


# This should really be a singleton
class LogicalTypeSymbol(HolTypeSymbol):
    @override
    def get_kind_string(self) -> str:
        return 'logical type'


class SortSymbol(HolTypeSymbol):
    @override
    def get_kind_string(self) -> str:
        return 'sort'


class LogicalConstantSymbol(ConstantTermSymbol):
    @override
    def get_kind_string(self) -> str:
        return 'logical constant'


@dataclass(frozen=True)
class NonLogicalConstantSymbol(ConstantTermSymbol):
    type: SimpleType

    @override
    def get_kind_string(self) -> str:
        return 'nonlogical constant'


HolSignatureSymbol = SortSymbol | NonLogicalConstantSymbol
HolSymbol = LogicalTypeSymbol | LogicalConstantSymbol | HolSignatureSymbol
