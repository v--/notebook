from dataclasses import dataclass

from ..alphabet import BinaryConnective, PropConstantSymbol, Quantifier, UnaryPrefix
from ..signature import PredicateSymbol
from ..terms import SyntacticApplication, Term, Variable


@dataclass(frozen=True)
class PropConstant:
    value: PropConstantSymbol

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"parse_formula('{self}')"


@dataclass(frozen=True)
class EqualityFormula:
    left: Term
    right: Term

    def __str__(self) -> str:
        return f'({self.left} = {self.right})'

    def __repr__(self) -> str:
        return f"parse_formula('{self}')"


class PredicateApplication(SyntacticApplication[Term]):
    symbol: PredicateSymbol

    def __repr__(self) -> str:
        return f"parse_formula('{self}')"


@dataclass(frozen=True)
class NegationFormula:
    body: Formula

    def __str__(self) -> str:
        return f'{UnaryPrefix.NEGATION}{self.body}'

    def __repr__(self) -> str:
        return f"parse_formula('{self}')"


@dataclass(frozen=True)
class ConnectiveFormula:
    conn: BinaryConnective
    left: Formula
    right: Formula

    def __str__(self) -> str:
        return f'({self.left} {self.conn} {self.right})'

    def __repr__(self) -> str:
        return f"parse_formula('{self}')"


@dataclass(frozen=True)
class QuantifierFormula:
    quant: Quantifier
    var: Variable
    body: Formula

    def __str__(self) -> str:
        return f'{self.quant.value}{self.var}.{self.body}'

    def __repr__(self) -> str:
        return f"parse_formula('{self}')"


AtomicFormula = PropConstant | EqualityFormula | PredicateApplication
Formula = AtomicFormula | NegationFormula | ConnectiveFormula | QuantifierFormula
