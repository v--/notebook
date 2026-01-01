import functools

from ..formulas import ConnectiveFormula, NegationFormula, PredicateApplication, PropConstant
from .symbols import PropVariableSymbol


@functools.total_ordering
class PropVariable(PredicateApplication):
    symbol: PropVariableSymbol

    def __init__(self, symbol: PropVariableSymbol) -> None:
        super().__init__(symbol, [])

    def __lt__(self, other: PropVariable) -> bool:
        return self.symbol <= other.symbol

    def __repr__(self) -> str:
        return f"parse_prop_formula('{self}')"


class PropNegationFormula(NegationFormula):
    body: PropFormula

    def __repr__(self) -> str:
        return f"parse_prop_formula('{self}')"


class PropConnectiveFormula(ConnectiveFormula):
    left: PropFormula
    right: PropFormula

    def __repr__(self) -> str:
        return f"parse_prop_formula('{self}')"


PropFormula = PropConstant | PropVariable | PropNegationFormula | PropConnectiveFormula
