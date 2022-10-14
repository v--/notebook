from __future__ import annotations
from dataclasses import dataclass

from .tokens import SingletonFOLToken


@dataclass
class Variable:
    name: str

    def __str__(self):
        return self.name


@dataclass
class FunctionTerm:
    name: str
    arguments: list[Term]

    def __str__(self):
        arg_list = ', '.join(str(arg) for arg in self.arguments)
        return f'{self.name}({arg_list})'


Term = Variable | FunctionTerm


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
    conn: SingletonFOLToken
    a: Formula
    b: Formula

    def __str__(self):
        return f'({self.a} {self.conn} {self.b})'


@dataclass
class QuantifierFormula:
    quantifier: SingletonFOLToken
    variable: Variable
    sub: Formula

    def __str__(self):
        return f'{self.quantifier.value}{self.variable}.{self.sub}'


Formula = EqualityFormula | PredicateFormula | NegationFormula | ConnectiveFormula | QuantifierFormula
