from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..signature import BaseTypeSymbol, ConstantTermSymbol, LambdaSignature, SignatureSymbol
from .exceptions import HolSignatureError
from .symbols import (
    LogicalConstantSymbol,
    LogicalTypeSymbol,
    NonLogicalConstantSymbol,
    SortSymbol,
    common_constants,
    common_types,
)


if TYPE_CHECKING:
    from collections.abc import Iterator, MutableMapping

    from ..types import SimpleType


@dataclass
class HolSignature(LambdaSignature):
    _assignment: MutableMapping[ConstantTermSymbol, SimpleType]

    def __init__(self, *symbols: SortSymbol) -> None:
        super().__init__()
        super().add_symbol(common_types.prop)
        super().add_symbol(common_constants.verum)
        super().add_symbol(common_constants.falsum)
        super().add_symbol(common_constants.negation)
        super().add_symbol(common_constants.conjunction)
        super().add_symbol(common_constants.disjunction)
        super().add_symbol(common_constants.conditional)
        super().add_symbol(common_constants.biconditional)
        super().add_symbol(common_constants.equality)
        super().add_symbol(common_constants.forall)
        super().add_symbol(common_constants.exists)

        for sym in symbols:
            super().add_symbol(sym)

        self._assignment = {}

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

    def get_logical_type_symbol(self, name: str) -> LogicalTypeSymbol:
        sym = self[name]

        if not isinstance(sym, LogicalTypeSymbol):
            raise HolSignatureError(f'Expected {name} to be a logical type symbol, but got a {sym.get_kind_string()}')

        return sym

    def get_sort_symbol(self, name: str) -> SortSymbol:
        sym = self[name]

        if not isinstance(sym, SortSymbol):
            raise HolSignatureError(f'Expected {name} to be a sort, but got a {sym.get_kind_string()}')

        return sym

    def get_logical_constant_symbol(self, name: str) -> LogicalConstantSymbol:
        sym = self[name]

        if not isinstance(sym, LogicalConstantSymbol):
            raise HolSignatureError(f'Expected {name} to be a logical constant symbol, but got a {sym.get_kind_string()}')

        return sym

    def get_nonlogical_constant_symbol(self, name: str) -> NonLogicalConstantSymbol:
        sym = self[name]

        if not isinstance(sym, NonLogicalConstantSymbol):
            raise HolSignatureError(f'Expected {name} to be a nonlogical constant symbol, but got a {sym.get_kind_string()}')

        return sym

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


PLAIN_HOL_SIGNATURE = HolSignature(common_types.individual)
