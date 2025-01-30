from typing import NamedTuple

from ....parsing.identifiers import GreekIdentifier
from ..alphabet import BinaryConnective, Quantifier, SchemaConnective, UnaryConnective
from ..terms import ExtendedTermSchema, FunctionLikeTerm, TermSchema, VariablePlaceholder
from .formulas import ConstantFormula


class FormulaPlaceholder(NamedTuple):
    identifier: GreekIdentifier

    def __str__(self) -> str:
        return str(self.identifier)


class EqualityFormulaSchema(NamedTuple):
    a: TermSchema
    b: TermSchema

    def __str__(self) -> str:
        return f'({self.a} = {self.b})'


class PredicateFormulaSchema(FunctionLikeTerm[TermSchema]):
    pass


class NegationFormulaSchema(NamedTuple):
    sub: 'FormulaSchema'

    def __str__(self) -> str:
        return f'{UnaryConnective.negation}{self.sub}'


class ConnectiveFormulaSchema(NamedTuple):
    conn: BinaryConnective
    a: 'FormulaSchema'
    b: 'FormulaSchema'

    def __str__(self) -> str:
        return f'({self.a} {self.conn} {self.b})'


class QuantifierFormulaSchema(NamedTuple):
    quantifier: Quantifier
    variable: VariablePlaceholder
    sub: 'FormulaSchema'

    def __str__(self) -> str:
        return f'{self.quantifier.value}{self.variable}.{self.sub}'


FormulaSchema = FormulaPlaceholder | ConstantFormula | EqualityFormulaSchema | PredicateFormulaSchema | NegationFormulaSchema | ConnectiveFormulaSchema | QuantifierFormulaSchema


class SubstitutionSchema(NamedTuple):
    formula: FormulaSchema
    var: VariablePlaceholder
    dest: ExtendedTermSchema

    def __str__(self) -> str:
        return f'{self.formula}[{self.var} {SchemaConnective.substitution} {self.dest}]'


ExtendedFormulaSchema = FormulaSchema | SubstitutionSchema
