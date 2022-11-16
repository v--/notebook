from __future__ import annotations
from dataclasses import dataclass

from .tokens import BinaryConnective, Quantifier
from .terms import Variable, Term


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
        return f'{self.name}({args})'


@dataclass
class NegationFormula:
    sub: Formula

    def __str__(self):
        return f'¬{self.sub}'


@dataclass
class ConnectiveFormula:
    conn: BinaryConnective
    a: Formula
    b: Formula

    def __str__(self):
        return f'({self.a} {self.conn} {self.b})'


@dataclass
class QuantifierFormula:
    quantifier: Quantifier
    variable: Variable
    sub: Formula

    def __str__(self):
        return f'{self.quantifier.value}{self.variable}.{self.sub}'


Formula = EqualityFormula | PredicateFormula | NegationFormula | ConnectiveFormula | QuantifierFormula
