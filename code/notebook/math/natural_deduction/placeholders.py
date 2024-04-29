from typing import NamedTuple

from ..fol.alphabet import BinaryConnective, PropConstant, Quantifier
from ..fol.terms import Variable


class AtomicFormulaPlaceholder(NamedTuple):
    name: str

    def __str__(self) -> str:
        return self.name


class ConstantFormulaPlaceholder(NamedTuple):
    value: PropConstant

    def __str__(self) -> str:
        return str(self.value)


class NegationFormulaPlaceholder(NamedTuple):
    sub: 'FormulaPlaceholder'

    def __str__(self) -> str:
        return f'¬{self.sub}'


class ConnectiveFormulaPlaceholder(NamedTuple):
    conn: BinaryConnective
    a: 'FormulaPlaceholder'
    b: 'FormulaPlaceholder'

    def __str__(self) -> str:
        return f'({self.a} {self.conn} {self.b})'


class QuantifierFormulaPlaceholder(NamedTuple):
    quantifier: Quantifier
    variable: Variable
    sub: 'FormulaPlaceholder'

    def __str__(self) -> str:
        return f'{self.quantifier.value}{self.variable}.{self.sub}'


FormulaPlaceholder = AtomicFormulaPlaceholder | ConstantFormulaPlaceholder | NegationFormulaPlaceholder | ConnectiveFormulaPlaceholder | QuantifierFormulaPlaceholder
