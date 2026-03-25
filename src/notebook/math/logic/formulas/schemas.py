from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..alphabet import BinaryConnective, Quantifier, UnaryPrefix
from ..terms import SyntacticApplication, TermSchema, VariablePlaceholder
from .formulas import PropConstant


if TYPE_CHECKING:
    from ....parsing.identifiers import GreekIdentifier
    from ..signature import PredicateSymbol


@dataclass(frozen=True)
class FormulaPlaceholder:
    identifier: GreekIdentifier

    def __str__(self) -> str:
        return str(self.identifier)

    def __repr__(self) -> str:
        return f"parse_formula_schema('{self}')"


@dataclass(frozen=True)
class EqualityFormulaSchema:
    left: TermSchema
    right: TermSchema

    def __str__(self) -> str:
        return f'({self.left} = {self.right})'

    def __repr__(self) -> str:
        return f"parse_formula_schema('{self}')"


class PredicateApplicationSchema(SyntacticApplication[TermSchema]):
    symbol: PredicateSymbol

    def __repr__(self) -> str:
        return f"parse_formula_schema('{self}')"


@dataclass(frozen=True)
class NegationFormulaSchema:
    body: FormulaSchema

    def __str__(self) -> str:
        return f'{UnaryPrefix.NEGATION}{self.body}'

    def __repr__(self) -> str:
        return f"parse_formula_schema('{self}')"


@dataclass(frozen=True)
class ConnectiveFormulaSchema:
    conn: BinaryConnective
    left: FormulaSchema
    right: FormulaSchema

    def __str__(self) -> str:
        return f'({self.left} {self.conn} {self.right})'

    def __repr__(self) -> str:
        return f"parse_formula_schema('{self}')"


@dataclass(frozen=True)
class QuantifierFormulaSchema:
    quant: Quantifier
    var: VariablePlaceholder
    body: FormulaSchema

    def __str__(self) -> str:
        return f'{self.quant.value}{self.var}.{self.body}'

    def __repr__(self) -> str:
        return f"parse_formula_schema('{self}')"


AtomicFormulaSchema = PropConstant | EqualityFormulaSchema | PredicateApplicationSchema
FormulaSchema = AtomicFormulaSchema | FormulaPlaceholder | NegationFormulaSchema | ConnectiveFormulaSchema | QuantifierFormulaSchema
