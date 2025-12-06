from typing import override

from ..signature import (
    FormalLogicSignature,
    FormalLogicSignatureError,
    SignatureSymbol,
)
from .variables import PropositionalVariable


class PropositionalLogicSignature(FormalLogicSignature):
    @override
    def add_symbol(self, symbol: SignatureSymbol) -> None:
        if isinstance(symbol, PropositionalVariable):
            super().add_symbol(symbol)
        else:
            raise FormalLogicSignatureError(f'Cannot add the {symbol.get_kind_string()} symbol {symbol} to a propositional signature')

    def get_propositional_variable(self, name: str) -> PropositionalVariable:
        sym = self[name]

        if not isinstance(sym, PropositionalVariable):
            raise FormalLogicSignatureError(f'Expected {name} to be a propositional variable symbol, but got a {sym.get_kind_string()}')

        return sym


PROPOSITIONAL_SIGNATURE = PropositionalLogicSignature(
    *(PropositionalVariable(chr(i)) for i in range(ord('a'), ord('z') + 1))
)


DEFAULT_PROPOSITIONAL_VARIABLE = PROPOSITIONAL_SIGNATURE.get_propositional_variable('p')
