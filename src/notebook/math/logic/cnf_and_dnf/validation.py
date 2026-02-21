from ..alphabet import BinaryConnective, LatticeConnective, get_dual_connective
from ..formulas import (
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
def is_inner_cnf_or_dnf_formula(formula: Formula, outer: LatticeConnective) -> bool:
    if isinstance(formula, PropConstant) or is_literal(formula):
        return True

    inner = get_dual_connective(outer)

    return (
        isinstance(formula, ConnectiveFormula) and
        formula.conn == inner and
        is_inner_cnf_or_dnf_formula(formula.left, outer) and
        is_inner_cnf_or_dnf_formula(formula.right, outer)
    )


def is_formula_in_cnf_or_dnf(formula: Formula, outer: LatticeConnective) -> bool:
    if is_inner_cnf_or_dnf_formula(formula, outer):
        return True

    return (
        isinstance(formula, ConnectiveFormula) and
        formula.conn == outer and
        is_formula_in_cnf_or_dnf(formula.left, outer) and
        is_formula_in_cnf_or_dnf(formula.right, outer)
    )


def is_formula_in_cnf(formula: Formula) -> bool:
    return is_formula_in_cnf_or_dnf(formula, outer=BinaryConnective.CONJUNCTION)


def is_formula_in_dnf(formula: Formula) -> bool:
    return is_formula_in_cnf_or_dnf(formula, outer=BinaryConnective.DISJUNCTION)
