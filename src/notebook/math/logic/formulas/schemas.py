from dataclasses import dataclass

from ....parsing.identifiers import GreekIdentifier
from ..alphabet import BinaryConnective, Quantifier, UnaryPrefix
from ..terms import SyntacticApplication, TermSchema, VariablePlaceholder
from .formulas import ConstantFormula


@dataclass(frozen=True)
class FormulaPlaceholder:
    identifier: GreekIdentifier

    def __str__(self) -> str:
        return str(self.identifier)


@dataclass(frozen=True)
class EqualityFormulaSchema:
    left: TermSchema
    right: TermSchema

    def __str__(self) -> str:
        return f'({self.left} = {self.right})'


class PredicateApplicationSchema(SyntacticApplication[TermSchema]):
    pass


@dataclass(frozen=True)
class NegationFormulaSchema:
    body: FormulaSchema

    def __str__(self) -> str:
        return f'{UnaryPrefix.NEGATION}{self.body}'


@dataclass(frozen=True)
class ConnectiveFormulaSchema:
    conn: BinaryConnective
    left: FormulaSchema
    right: FormulaSchema

    def __str__(self) -> str:
        return f'({self.left} {self.conn} {self.right})'


@dataclass(frozen=True)
class QuantifierFormulaSchema:
    quantifier: Quantifier
    var: VariablePlaceholder
    body: FormulaSchema

    def __str__(self) -> str:
        return f'{self.quantifier.value}{self.var}.{self.body}'


FormulaSchema = FormulaPlaceholder | ConstantFormula | EqualityFormulaSchema | PredicateApplicationSchema | NegationFormulaSchema | ConnectiveFormulaSchema | QuantifierFormulaSchema
