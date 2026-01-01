from ...alphabet import BinaryConnective, LatticeConnective, get_dual_connective
from ...formulas import (
    AtomicFormula,
    ConnectiveFormula,
    EqualityFormula,
    Formula,
    NegationFormula,
    PredicateApplication,
    PropConstant,
)


def is_literal(formula: Formula) -> bool:
    if isinstance(formula, EqualityFormula | PredicateApplication):
        return True

    return isinstance(formula, NegationFormula) and isinstance(formula.body, AtomicFormula)


# These are elementary disjunctions/conjunctions
def is_inner_polynomial_formula(formula: Formula, inner: LatticeConnective) -> bool:
    if isinstance(formula, PropConstant) or is_literal(formula):
        return True

    return (
        isinstance(formula, ConnectiveFormula) and
        formula.conn == inner and
        is_inner_polynomial_formula(formula.left, inner) and
        is_inner_polynomial_formula(formula.right, inner)
    )


def is_formula_in_polynomial_form(formula: Formula, inner: LatticeConnective) -> bool:
    if is_inner_polynomial_formula(formula, inner):
        return True

    outer = get_dual_connective(inner)

    return (
        isinstance(formula, ConnectiveFormula) and
        formula.conn == outer and
        is_formula_in_polynomial_form(formula.left, inner) and
        is_formula_in_polynomial_form(formula.right, inner)
    )


def is_formula_in_cnf(formula: Formula) -> bool:
    return is_formula_in_polynomial_form(formula, inner=BinaryConnective.DISJUNCTION)


def is_formula_in_dnf(formula: Formula) -> bool:
    return is_formula_in_polynomial_form(formula, inner=BinaryConnective.CONJUNCTION)
