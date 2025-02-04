from dataclasses import dataclass
from typing import TypeGuard

from ..alphabet import BinaryConnective, PropConstant, Quantifier, UnaryConnective
from ..terms import FunctionLikeTerm, Term, Variable


@dataclass(frozen=True)
class ConstantFormula:
    value: PropConstant

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class EqualityFormula:
    a: Term
    b: Term

    def __str__(self) -> str:
        return f'({self.a} = {self.b})'


class PredicateFormula(FunctionLikeTerm[Term]):
    pass


@dataclass(frozen=True)
class NegationFormula:
    sub: 'Formula'

    def __str__(self) -> str:
        return f'{UnaryConnective.negation}{self.sub}'


@dataclass(frozen=True)
class ConnectiveFormula:
    conn: BinaryConnective
    a: 'Formula'
    b: 'Formula'

    def __str__(self) -> str:
        return f'({self.a} {self.conn} {self.b})'


@dataclass(frozen=True)
class QuantifierFormula:
    quantifier: Quantifier
    var: Variable
    sub: 'Formula'

    def __str__(self) -> str:
        return f'{self.quantifier.value}{self.var}.{self.sub}'


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
