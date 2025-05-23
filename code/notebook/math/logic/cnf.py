import inspect
import itertools
from collections.abc import Callable, Sequence

from .alphabet import BinaryConnective, PropConstant
from .formulas import (
    ConnectiveFormula,
    ConstantFormula,
    Formula,
    FormulaTransformationVisitor,
    FormulaVisitor,
    NegationFormula,
    PredicateFormula,
    QuantifierFormula,
    is_atomic,
    is_conjunction,
    is_disjunction,
)
from .pnf import is_formula_quantifierless, move_negations, remove_conditionals


def is_literal(formula: Formula) -> bool:
    return is_atomic(formula) or (isinstance(formula, NegationFormula) and is_atomic(formula.sub))


def is_elementary_disjunction(formula: Formula) -> bool:
    if is_literal(formula):
        return True

    return is_disjunction(formula) and is_elementary_disjunction(formula.a) and is_elementary_disjunction(formula.b)


def is_formula_in_cnf(formula: Formula) -> bool:
    if is_elementary_disjunction(formula):
        return True

    return is_conjunction(formula) and is_formula_in_cnf(formula.a) and is_formula_in_cnf(formula.b)


def connect_formulas(formulas: Sequence[Formula], conn: BinaryConnective) -> Formula:
    assert len(formulas) > 0

    if len(formulas) == 1:
        return formulas[0]

    return ConnectiveFormula(conn, connect_formulas(formulas[:-1], conn), formulas[-1])


class RemoveConstantsVisitor(FormulaTransformationVisitor):
    def visit_constant(self, formula: ConstantFormula) -> ConnectiveFormula:
        p = PredicateFormula('p', [])

        match formula.value:
            case PropConstant.VERUM:
                return ConnectiveFormula(BinaryConnective.DISJUNCTION, p, NegationFormula(p))

            case PropConstant.FALSUM:
                return ConnectiveFormula(BinaryConnective.CONJUNCTION, p, NegationFormula(p))


def remove_constants(formula: Formula) -> Formula:
    return RemoveConstantsVisitor().visit(formula)


class HasReachableConjunctionVisitor(FormulaVisitor[bool]):
    def generic_visit(self, formula: Formula) -> bool:  # noqa: ARG002
        return False

    def visit_negation(self, formula: NegationFormula) -> bool:  # noqa: ARG002
        return False

    def visit_connective(self, formula: ConnectiveFormula) -> bool:
        match formula.conn:
            case BinaryConnective.DISJUNCTION:
                return self.visit(formula.a) or self.visit(formula.b)

            case BinaryConnective.CONJUNCTION:
                    return True

            case _:
                    return False

    def visit_quantifier(self, formula: QuantifierFormula) -> bool:
        return self.visit(formula.sub)


def has_reachable_conjunction(formula: Formula) -> bool:
    return HasReachableConjunctionVisitor().visit(formula)


class PullConjunctionVisitor(FormulaTransformationVisitor):
    def visit_connective(self, formula: ConnectiveFormula) -> ConnectiveFormula:
        a = self.visit(formula.a)

        if is_disjunction(formula) and is_conjunction(a):
            return ConnectiveFormula(
                BinaryConnective.CONJUNCTION,
                self.visit(ConnectiveFormula(BinaryConnective.DISJUNCTION, a.a, formula.b)),
                self.visit(ConnectiveFormula(BinaryConnective.DISJUNCTION, a.b, formula.b))
            )

        b = self.visit(formula.b)

        if is_disjunction(formula) and is_conjunction(b):
            return ConnectiveFormula(
                BinaryConnective.CONJUNCTION,
                self.visit(ConnectiveFormula(BinaryConnective.DISJUNCTION, formula.a, b.a)),
                self.visit(ConnectiveFormula(BinaryConnective.DISJUNCTION, formula.a, b.b))
            )

        return ConnectiveFormula(formula.conn, a, b)


def pull_conjunction(formula: Formula) -> Formula:
    return PullConjunctionVisitor().visit(formula)


# This is alg:cnf_and_dnf in the monograph
def to_cnf(formula: Formula) -> Formula:
    assert is_formula_quantifierless(formula)
    return pull_conjunction(move_negations(remove_conditionals(remove_constants(formula))))


# This is alg:full_cnf_and_dnf in the monograph
def function_to_cnf(fun: Callable[..., bool]) -> Formula:
    fun_params = inspect.signature(fun).parameters

    if len(fun_params) == 0:
        p = PredicateFormula('p', ())
        return ConnectiveFormula(
            BinaryConnective.DISJUNCTION if fun() else BinaryConnective.CONJUNCTION,
            p,
            NegationFormula(p)
        )

    for param in fun_params.values():
        assert all('a' <= c <= 'z' for c in param.name), \
            f'In order to become a valid predicate name, the parameter name {param.name!r} must consist only of small Latin characters.'

    # These names will generate valid formulas only when they consist of Latin letters
    predicates = [PredicateFormula(param.name, ()) for param in fun_params.values()]
    disjuncts = list[Formula](
        connect_formulas(
            [NegationFormula(p) if arg else p for p, arg in zip(predicates, arg_tuple, strict=True)],
            BinaryConnective.DISJUNCTION
        )
        for arg_tuple in itertools.product([False, True], repeat=len(fun_params))
        if fun(*arg_tuple) is False
    )

    if len(disjuncts) == 0:  # fun is vacuously true
        p = predicates[0]
        return ConnectiveFormula(BinaryConnective.DISJUNCTION, p, NegationFormula(p))

    return connect_formulas(disjuncts, BinaryConnective.CONJUNCTION)
