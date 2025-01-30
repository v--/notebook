from typing import NamedTuple, TypeGuard

from ..alphabet import BinaryConnective, PropConstant, Quantifier, UnaryConnective
from ..terms import FunctionLikeTerm, Term, Variable


class ConstantFormula(NamedTuple):
    value: PropConstant

    def __str__(self) -> str:
        return str(self.value)


class EqualityFormula(NamedTuple):
    a: Term
    b: Term

    def __str__(self) -> str:
        return f'({self.a} = {self.b})'


class PredicateFormula(FunctionLikeTerm[Term]):
    pass


class NegationFormula(NamedTuple):
    sub: 'Formula'

    def __str__(self) -> str:
        return f'{UnaryConnective.negation}{self.sub}'


class ConnectiveFormula(NamedTuple):
    conn: BinaryConnective
    a: 'Formula'
    b: 'Formula'

    def __str__(self) -> str:
        return f'({self.a} {self.conn} {self.b})'


class QuantifierFormula(NamedTuple):
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
