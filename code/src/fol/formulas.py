from dataclasses import dataclass
from typing import TypeGuard

from .tokens import BinaryConnective, Quantifier, PropConstant
from .terms import Variable, Term


@dataclass
class ConstantFormula:
    value: PropConstant

    def __str__(self):
        return str(self.value)


@dataclass
class EqualityFormula:
    a: Term
    b: Term

    def __str__(self):
        return f'({self.a} = {self.b})'


@dataclass
class PredicateFormula:
    name: str
    arguments: list[Term]

    def __str__(self):
        args = ', '.join(str(arg) for arg in self.arguments)
        return f'{self.name}({args})' if len(args) > 0 else self.name


@dataclass
class NegationFormula:
    sub: 'Formula'

    def __str__(self):
        return f'¬{self.sub}'


@dataclass
class ConnectiveFormula:
    conn: BinaryConnective
    a: 'Formula'
    b: 'Formula'

    def __str__(self):
        return f'({self.a} {self.conn} {self.b})'


@dataclass
class QuantifierFormula:
    quantifier: Quantifier
    variable: Variable
    sub: 'Formula'

    def __str__(self):
        return f'{self.quantifier.value}{self.variable}.{self.sub}'


Formula = ConstantFormula | EqualityFormula | PredicateFormula | NegationFormula | ConnectiveFormula | QuantifierFormula

def is_atomic(formula: Formula) -> TypeGuard[ConstantFormula | EqualityFormula | PredicateFormula]:
    return isinstance(formula, ConstantFormula | EqualityFormula | PredicateFormula)

def is_disjunction(formula: Formula) -> TypeGuard[ConnectiveFormula]:
    return isinstance(formula, ConnectiveFormula) and formula.conn == BinaryConnective.disjunction

def is_conjunction(formula: Formula) -> TypeGuard[ConnectiveFormula]:
    return isinstance(formula, ConnectiveFormula) and formula.conn == BinaryConnective.conjunction

def is_conditional(formula: Formula) -> TypeGuard[ConnectiveFormula]:
    return isinstance(formula, ConnectiveFormula) and formula.conn == BinaryConnective.conditional

def is_biconditional(formula: Formula) -> TypeGuard[ConnectiveFormula]:
    return isinstance(formula, ConnectiveFormula) and formula.conn == BinaryConnective.biconditional
