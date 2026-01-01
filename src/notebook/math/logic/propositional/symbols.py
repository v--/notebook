import functools
from typing import override

from ....parsing import is_greek_identifier, is_latin_identifier
from ....support.unicode import Capitalization
from ..signature import (
    FormalLogicSignatureError,
    PredicateSymbol,
    SignatureSymbolNotation,
)


@functools.total_ordering
class PropVariableSymbol(PredicateSymbol):
    def __init__(self, name: str) -> None:
        super().__init__(name, arity=0, notation='CONDENSED')

    def __lt__(self, other: PropVariableSymbol) -> bool:
        return self.name <= other.name

    @override
    def get_kind_string(self) -> str:
        return 'propositional variable'

    @override
    def validate(self, name: str, arity: int, notation: SignatureSymbolNotation | None = None) -> None:
        if not is_latin_identifier(name, Capitalization.LOWER) and not is_greek_identifier(name, Capitalization.LOWER):
            raise FormalLogicSignatureError('Propositional variables are only allowed to be lowercase Latin or Greek identifiers')
