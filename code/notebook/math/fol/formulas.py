from collections.abc import Sequence
from typing import NamedTuple, TypeGuard

from .alphabet import BinaryConnective, PropConstant, Quantifier
from .terms import Term, Variable


class ConstantFormula(NamedTuple):
    value: PropConstant

    def __str__(self) -> str:
        return str(self.value)


class EqualityFormula(NamedTuple):
    a: Term
    b: Term

    def __str__(self) -> str:
        return f'({self.a} = {self.b})'


class PredicateFormula(NamedTuple):
    name: str
    arguments: Sequence[Term]

    def __str__(self) -> str:
        args = ', '.join(str(arg) for arg in self.arguments)
        return f'{self.name}({args})' if len(args) > 0 else self.name


class NegationFormula(NamedTuple):
    sub: 'Formula'

    def __str__(self) -> str:
        return f'¬{self.sub}'


class ConnectiveFormula(NamedTuple):
    conn: BinaryConnective
    a: 'Formula'
    b: 'Formula'

    def __str__(self) -> str:
        return f'({self.a} {self.conn} {self.b})'


class QuantifierFormula(NamedTuple):
    quantifier: Quantifier
    variable: Variable
    sub: 'Formula'

    def __str__(self) -> str:
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


def is_subformula(formula: Formula, subformula: Formula) -> bool:
    if formula == subformula:
        return True

    match formula:
        case NegationFormula():
            return is_subformula(formula.sub, subformula)

        case ConnectiveFormula():
            return is_subformula(formula.a, subformula) or is_subformula(formula.b, subformula)

        case QuantifierFormula():
            return is_subformula(formula.sub, subformula)

    return False
