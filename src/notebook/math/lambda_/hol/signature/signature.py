from typing import TYPE_CHECKING

from notebook.math.lambda_.hol.alphabet import LogicalConstantName, LogicalTypeName, SortName
from notebook.math.lambda_.signature import BaseTypeSymbol, ConstantTermSymbol, LambdaSignature, SignatureSymbol

from .exceptions import HolSignatureError
from .symbols import (
    HolSignatureSymbol,
    LogicalConstantSymbol,
    LogicalTypeSymbol,
    NonLogicalConstantSymbol,
    SortSymbol,
)


if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator


class HolSignature(LambdaSignature):
    def __init__(self, *symbols: SortSymbol | NonLogicalConstantSymbol) -> None:
        super().__init__()
        super().add_symbol(LogicalTypeSymbol(LogicalTypeName.PROP))
        super().add_symbol(LogicalConstantSymbol(LogicalConstantName.VERUM))
        super().add_symbol(LogicalConstantSymbol(LogicalConstantName.FALSUM))
        super().add_symbol(LogicalConstantSymbol(LogicalConstantName.NEGATION))
        super().add_symbol(LogicalConstantSymbol(LogicalConstantName.CONJUNCTION))
        super().add_symbol(LogicalConstantSymbol(LogicalConstantName.DISJUNCTION))
        super().add_symbol(LogicalConstantSymbol(LogicalConstantName.CONDITIONAL))
        super().add_symbol(LogicalConstantSymbol(LogicalConstantName.BICONDITIONAL))
        super().add_symbol(LogicalConstantSymbol(LogicalConstantName.EQUALITY))
        super().add_symbol(LogicalConstantSymbol(LogicalConstantName.FORALL))
        super().add_symbol(LogicalConstantSymbol(LogicalConstantName.EXISTS))

        for sym in symbols:
            self.add_symbol(sym)

    def add_symbol(self, symbol: SignatureSymbol) -> None:
        match symbol:
            case ConstantTermSymbol():
                if not isinstance(symbol, NonLogicalConstantSymbol):
                    raise HolSignatureError('Only non-logical constant symbols can be added')

                super().add_symbol(symbol)

            case BaseTypeSymbol():
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

    def iter_sorts(self) -> Iterator[SortSymbol]:
        for sym in super().__iter__():
            if isinstance(sym, SortSymbol):
                yield sym

    def iter_nonlogical(self) -> Iterable[NonLogicalConstantSymbol]:
        for sym in super().__iter__():
            if isinstance(sym, NonLogicalConstantSymbol):
                yield sym

    def __iter__(self) -> Iterator[HolSignatureSymbol]:
        yield from self.iter_sorts()
        yield from self.iter_nonlogical()


PLAIN_HOL_SIGNATURE = HolSignature(SortSymbol(SortName.INDIVIDUAL))
