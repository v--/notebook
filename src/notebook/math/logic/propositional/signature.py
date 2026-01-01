from typing import override

from ..signature import (
    FormalLogicSignature,
    FormalLogicSignatureError,
    SignatureSymbol,
)
from .formulas import PropVariable
from .symbols import PropVariableSymbol


class PropLogicSignature(FormalLogicSignature):
    @override
    def add_symbol(self, symbol: SignatureSymbol) -> None:
        if isinstance(symbol, PropVariableSymbol):
            super().add_symbol(symbol)
        else:
            raise FormalLogicSignatureError(f'Cannot add the {symbol.get_kind_string()} symbol {symbol} to a propositional signature')

    def get_prop_variable_symbol(self, name: str) -> PropVariableSymbol:
        sym = self[name]

        if not isinstance(sym, PropVariableSymbol):
            raise FormalLogicSignatureError(f'Expected {name} to be a propositional variable symbol, but got a {sym.get_kind_string()}')

        return sym

    def get_prop_variable(self, name: str) -> PropVariable:
        return PropVariable(self.get_prop_variable_symbol(name))


DEFAULT_PROP_SIGNATURE = PropLogicSignature(
    *(PropVariableSymbol(chr(i)) for i in range(ord('a'), ord('z') + 1))
)


DEFAULT_PROP_VARIABLE = DEFAULT_PROP_SIGNATURE.get_prop_variable('p')
