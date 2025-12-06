from dataclasses import dataclass
from typing import TypeGuard

from ..alphabet import BinaryConnective, PropConstant, Quantifier, UnaryPrefix
from ..signature import PredicateSymbol
from ..terms import SyntacticApplication, Term, Variable


@dataclass(frozen=True)
class ConstantFormula:
    value: PropConstant

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"parse_formula('{self}')"


@dataclass(frozen=True)
class EqualityFormula:
    left: Term
    right: Term

    def __str__(self) -> str:
        return f'({self.left} = {self.right})'

    def __repr__(self) -> str:
        return f"parse_formula('{self}')"


class PredicateApplication(SyntacticApplication[Term]):
    symbol: PredicateSymbol

    def __repr__(self) -> str:
        return f"parse_formula('{self}')"


@dataclass(frozen=True)
class NegationFormula:
    body: Formula

    def __str__(self) -> str:
        return f'{UnaryPrefix.NEGATION}{self.body}'

    def __repr__(self) -> str:
        return f"parse_formula('{self}')"


@dataclass(frozen=True)
class ConnectiveFormula:
    conn: BinaryConnective
    left: Formula
    right: Formula

    def __str__(self) -> str:
        return f'({self.left} {self.conn} {self.right})'

    def __repr__(self) -> str:
        return f"parse_formula('{self}')"


@dataclass(frozen=True)
class QuantifierFormula:
    quantifier: Quantifier
    var: Variable
    body: Formula

    def __str__(self) -> str:
        return f'{self.quantifier.value}{self.var}.{self.body}'

    def __repr__(self) -> str:
        return f"parse_formula('{self}')"


Formula = ConstantFormula | EqualityFormula | PredicateApplication | NegationFormula | ConnectiveFormula | QuantifierFormula


def is_logical_constant(formula: Formula) -> TypeGuard[ConstantFormula]:
    return isinstance(formula, ConstantFormula)


def is_predicate_application(formula: Formula) -> TypeGuard[PredicateApplication]:
    return isinstance(formula, PredicateApplication)


def is_atomic(formula: Formula) -> TypeGuard[ConstantFormula | EqualityFormula | PredicateApplication]:
    return isinstance(formula, ConstantFormula | EqualityFormula | PredicateApplication)


def is_negation(formula: Formula) -> TypeGuard[NegationFormula]:
    return isinstance(formula, NegationFormula)


def is_disjunction(formula: Formula) -> TypeGuard[ConnectiveFormula]:
    return isinstance(formula, ConnectiveFormula) and formula.conn == BinaryConnective.DISJUNCTION


def is_conjunction(formula: Formula) -> TypeGuard[ConnectiveFormula]:
    return isinstance(formula, ConnectiveFormula) and formula.conn == BinaryConnective.CONJUNCTION


def is_conditional(formula: Formula) -> TypeGuard[ConnectiveFormula]:
    return isinstance(formula, ConnectiveFormula) and formula.conn == BinaryConnective.CONDITIONAL


def is_biconditional(formula: Formula) -> TypeGuard[ConnectiveFormula]:
    return isinstance(formula, ConnectiveFormula) and formula.conn == BinaryConnective.BICONDITIONAL
