from dataclasses import dataclass

from ....parsing.identifiers import GreekIdentifier
from ..alphabet import BinaryConnective, Quantifier, SchemaConnective, UnaryConnective
from ..terms import ExtendedTermSchema, FunctionLikeTerm, TermSchema, VariablePlaceholder
from .formulas import ConstantFormula


@dataclass(frozen=True)
class FormulaPlaceholder:
    identifier: GreekIdentifier

    def __str__(self) -> str:
        return str(self.identifier)


@dataclass(frozen=True)
class EqualityFormulaSchema:
    a: TermSchema
    b: TermSchema

    def __str__(self) -> str:
        return f'({self.a} = {self.b})'


class PredicateFormulaSchema(FunctionLikeTerm[TermSchema]):
    pass


@dataclass(frozen=True)
class NegationFormulaSchema:
    sub: 'FormulaSchema'

    def __str__(self) -> str:
        return f'{UnaryConnective.NEGATION}{self.sub}'


@dataclass(frozen=True)
class ConnectiveFormulaSchema:
    conn: BinaryConnective
    a: 'FormulaSchema'
    b: 'FormulaSchema'

    def __str__(self) -> str:
        return f'({self.a} {self.conn} {self.b})'


@dataclass(frozen=True)
class QuantifierFormulaSchema:
    quantifier: Quantifier
    variable: VariablePlaceholder
    sub: 'FormulaSchema'

    def __str__(self) -> str:
        return f'{self.quantifier.value}{self.variable}.{self.sub}'


FormulaSchema = FormulaPlaceholder | ConstantFormula | EqualityFormulaSchema | PredicateFormulaSchema | NegationFormulaSchema | ConnectiveFormulaSchema | QuantifierFormulaSchema


@dataclass(frozen=True)
class SubstitutionSchema:
    formula: FormulaSchema
    var: VariablePlaceholder
    dest: ExtendedTermSchema

    def __str__(self) -> str:
        return f'{self.formula}[{self.var} {SchemaConnective.SUBSTITUTION} {self.dest}]'


ExtendedFormulaSchema = FormulaSchema | SubstitutionSchema
