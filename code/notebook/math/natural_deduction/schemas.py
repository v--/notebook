from typing import NamedTuple

from ...parsing.identifiers import Identifier
from ..fol.alphabet import BinaryConnective, PropConstant, Quantifier
from ..fol.terms import Variable


class FormulaPlaceholder(NamedTuple):
    identifier: Identifier

    def __str__(self) -> str:
        return str(self.identifier)


class ConstantFormulaSchema(NamedTuple):
    value: PropConstant

    def __str__(self) -> str:
        return str(self.value)


class NegationFormulaSchema(NamedTuple):
    sub: 'FormulaSchema'

    def __str__(self) -> str:
        return f'¬{self.sub}'


class ConnectiveFormulaSchema(NamedTuple):
    conn: BinaryConnective
    a: 'FormulaSchema'
    b: 'FormulaSchema'

    def __str__(self) -> str:
        return f'({self.a} {self.conn} {self.b})'


class QuantifierFormulaSchema(NamedTuple):
    quantifier: Quantifier
    variable: Variable
    sub: 'FormulaSchema'

    def __str__(self) -> str:
        return f'{self.quantifier.value}{self.variable}.{self.sub}'


FormulaSchema = FormulaPlaceholder | ConstantFormulaSchema | NegationFormulaSchema | ConnectiveFormulaSchema | QuantifierFormulaSchema
