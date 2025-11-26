"""We only support propositional formulas encoded as first-order formulas with no terms and predicates acting as variables.
This deviates from the monograph, but implementing support for propositional variables will be of no use for us."""

from typing import override

from ...parsing import is_greek_identifier, is_latin_identifier
from ...support.unicode import Capitalization
from .signature import (
    FormalLogicSignature,
    FormalLogicSignatureError,
    PredicateSymbol,
    SignatureSymbol,
    SignatureSymbolNotation,
)


class PropositionalVariable(PredicateSymbol):
    @override
    def get_kind_string(self) -> str:
        return 'propositional variable'

    @override
    def validate(self, name: str, arity: int, notation: SignatureSymbolNotation | None = None) -> None:
        if not is_latin_identifier(name, Capitalization.LOWER) and not is_greek_identifier(name, Capitalization.LOWER):
            raise FormalLogicSignatureError('Propositional variables are only allowed to be lowercase Latin or Greek identifiers')

    def __init__(self, name: str) -> None:
        super().__init__(name, arity=0, notation='CONDENSED')


class PropositionalLogicSignature(FormalLogicSignature):
    @override
    def add_symbol(self, symbol: SignatureSymbol) -> None:
        if isinstance(symbol, PropositionalVariable):
            super().add_symbol(symbol)
        else:
            raise FormalLogicSignatureError(f'Cannot add the {symbol.get_kind_string()} symbol {symbol} to a propositional signature')


PROPOSITIONAL_SIGNATURE = PropositionalLogicSignature()

for ind in range(ord('a'), ord('z') + 1):
    PROPOSITIONAL_SIGNATURE.add_symbol(PropositionalVariable(chr(ind)))


DEFAULT_PROPOSITIONAL_VARIABLE = PROPOSITIONAL_SIGNATURE['p']
