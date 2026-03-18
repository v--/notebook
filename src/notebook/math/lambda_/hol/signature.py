from collections.abc import Iterator, MutableMapping
from dataclasses import dataclass

from ..signature import ConstantTermSymbol, LambdaSignature, SignatureSymbol
from ..types import SimpleType
from .exceptions import HolSignatureError
from .symbols import (
    INDIVIDUAL_TYPE_SYMBOL,
    PROP_TYPE_SYMBOL,
    BaseTypeSymbol,
    LogicalConstantSymbol,
    NonLogicalConstantSymbol,
    SortSymbol,
)


@dataclass
class HolSignature(LambdaSignature):
    _assignment: MutableMapping[ConstantTermSymbol, SimpleType]

    def __init__(self, *symbols: SortSymbol) -> None:
        super().__init__()
        super().add_symbol(PROP_TYPE_SYMBOL)
        super().add_symbol(LogicalConstantSymbol('H⊤'))
        super().add_symbol(LogicalConstantSymbol('H⊥'))
        super().add_symbol(LogicalConstantSymbol('H∧'))
        super().add_symbol(LogicalConstantSymbol('H∨'))
        super().add_symbol(LogicalConstantSymbol('H→'))
        super().add_symbol(LogicalConstantSymbol('H↔'))
        super().add_symbol(LogicalConstantSymbol('H='))
        super().add_symbol(LogicalConstantSymbol('H∀'))
        super().add_symbol(LogicalConstantSymbol('H∃'))
        super().add_symbol(LogicalConstantSymbol('H℩'))

        for sym in symbols:
            super().add_symbol(sym)

    def add_symbol(self, symbol: SignatureSymbol, type_sym: SimpleType | None = None) -> None:
        match symbol:
            case ConstantTermSymbol():
                if not isinstance(symbol, NonLogicalConstantSymbol):
                    raise HolSignatureError('Only non-logical constant symbols can be added')

                if type_sym is None:
                    raise HolSignatureError('Constant symbols must have an associated type')

                super().add_symbol(symbol)
                self._assignment[symbol] = type_sym

            case BaseTypeSymbol():
                if type_sym is not None:
                    raise HolSignatureError('Base types cannot have associated types')

                if not isinstance(symbol, SortSymbol):
                    raise HolSignatureError('Only sorts are allowed as base types')

                super().add_symbol(symbol)

    def get_type(self, symbol: NonLogicalConstantSymbol) -> SimpleType:
        if symbol not in self:
            raise HolSignatureError(f'The symbol {symbol} is not part of the signature')

        return self._assignment[symbol]

    def iter_sorts(self) -> Iterator[SortSymbol]:
        for sym in super().__iter__():
            if isinstance(sym, SortSymbol):
                yield sym

    def iter_nonlogical(self) -> Iterator[NonLogicalConstantSymbol]:
        for sym in super().__iter__():
            if isinstance(sym, NonLogicalConstantSymbol):
                yield sym


EMPTY_HOL_SIGNATURE = HolSignature(INDIVIDUAL_TYPE_SYMBOL)
