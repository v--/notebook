import functools
from typing import override

from ....parsing import is_greek_identifier, is_latin_identifier
from ....support.unicode import Capitalization
from ..formulas import PredicateApplication
from ..signature import (
    FormalLogicSignatureError,
    PredicateSymbol,
    SignatureSymbolNotation,
)
from .exceptions import NonPropositionalFormulaError


@functools.total_ordering
class PropositionalVariable(PredicateSymbol):
    def __init__(self, name: str) -> None:
        super().__init__(name, arity=0, notation='CONDENSED')

    def __lt__(self, other: PropositionalVariable) -> bool:
        return self.name <= other.name

    @override
    def get_kind_string(self) -> str:
        return 'propositional variable'

    @override
    def validate(self, name: str, arity: int, notation: SignatureSymbolNotation | None = None) -> None:
        if not is_latin_identifier(name, Capitalization.LOWER) and not is_greek_identifier(name, Capitalization.LOWER):
            raise FormalLogicSignatureError('Propositional variables are only allowed to be lowercase Latin or Greek identifiers')


PropositionalVariableFormula = PredicateApplication


def extract_variable(formula: PropositionalVariableFormula) -> PropositionalVariable:
    if not isinstance(formula.symbol, PropositionalVariable):
        raise NonPropositionalFormulaError(f'Invalid propositional variable {formula.symbol}')

    return formula.symbol
