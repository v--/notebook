from typing import NamedTuple

from ..fol.alphabet import BinaryConnective, PropConstant, Quantifier
from ..fol.terms import Variable


class AtomicFormulaPlaceholder(NamedTuple):
    name: str

    def __str__(self):
        return self.name


class ConstantFormulaPlaceholder(NamedTuple):
    value: PropConstant

    def __str__(self):
        return str(self.value)


class NegationFormulaPlaceholder(NamedTuple):
    sub: 'FormulaPlaceholder'

    def __str__(self):
        return f'¬{self.sub}'


class ConnectiveFormulaPlaceholder(NamedTuple):
    conn: BinaryConnective
    a: 'FormulaPlaceholder'
    b: 'FormulaPlaceholder'

    def __str__(self):
        return f'({self.a} {self.conn} {self.b})'


class QuantifierFormulaPlaceholder(NamedTuple):
    quantifier: Quantifier
    variable: Variable
    sub: 'FormulaPlaceholder'

    def __str__(self):
        return f'{self.quantifier.value}{self.variable}.{self.sub}'


FormulaPlaceholder = AtomicFormulaPlaceholder | ConstantFormulaPlaceholder | NegationFormulaPlaceholder | ConnectiveFormulaPlaceholder | QuantifierFormulaPlaceholder


class Premise(NamedTuple):
    main: FormulaPlaceholder
    discharge: FormulaPlaceholder | None

    def __str__(self):
        if self.discharge is None:
            return str(self.main)

        return f'[{self.discharge}] {self.main}'


class Rule(NamedTuple):
    name: str
    premises: list[Premise]
    conclusion: FormulaPlaceholder

    def __str__(self):
        if len(self.premises) > 0:
            premise_str = ', '.join(map(str, self.premises))
            return f'({self.name}) {premise_str} ⇛ {self.conclusion}'

        return f'({self.name}) ⇛ {self.conclusion}'
