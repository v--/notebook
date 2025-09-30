from dataclasses import dataclass
from typing import TypeGuard

from ..alphabet import BinaryConnective, PropConstant, Quantifier, UnaryPrefix
from ..terms import FunctionLikeTerm, Term, Variable


@dataclass(frozen=True)
class ConstantFormula:
    value: PropConstant

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class EqualityFormula:
    left: Term
    right: Term

    def __str__(self) -> str:
        return f'({self.left} = {self.right})'


class PredicateFormula(FunctionLikeTerm[Term]):
    pass


@dataclass(frozen=True)
class NegationFormula:
    body: 'Formula'

    def __str__(self) -> str:
        return f'{UnaryPrefix.NEGATION}{self.body}'


@dataclass(frozen=True)
class ConnectiveFormula:
    conn: BinaryConnective
    left: 'Formula'
    right: 'Formula'

    def __str__(self) -> str:
        return f'({self.left} {self.conn} {self.right})'


@dataclass(frozen=True)
class QuantifierFormula:
    quantifier: Quantifier
    var: Variable
    body: 'Formula'

    def __str__(self) -> str:
        return f'{self.quantifier.value}{self.var}.{self.body}'


Formula = ConstantFormula | EqualityFormula | PredicateFormula | NegationFormula | ConnectiveFormula | QuantifierFormula


def is_atomic(formula: Formula) -> TypeGuard[ConstantFormula | EqualityFormula | PredicateFormula]:
    return isinstance(formula, ConstantFormula | EqualityFormula | PredicateFormula)


def is_disjunction(formula: Formula) -> TypeGuard[ConnectiveFormula]:
    return isinstance(formula, ConnectiveFormula) and formula.conn == BinaryConnective.DISJUNCTION


def is_conjunction(formula: Formula) -> TypeGuard[ConnectiveFormula]:
    return isinstance(formula, ConnectiveFormula) and formula.conn == BinaryConnective.CONJUNCTION


def is_conditional(formula: Formula) -> TypeGuard[ConnectiveFormula]:
    return isinstance(formula, ConnectiveFormula) and formula.conn == BinaryConnective.CONDITIONAL


def is_biconditional(formula: Formula) -> TypeGuard[ConnectiveFormula]:
    return isinstance(formula, ConnectiveFormula) and formula.conn == BinaryConnective.BICONDITIONAL
