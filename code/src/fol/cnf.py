from collections.abc import Callable
from typing import Sequence
import inspect
import itertools

from .tokens import BinaryConnective, PropConstant
from .formulas import Formula, ConstantFormula, PredicateFormula, NegationFormula, ConnectiveFormula, QuantifierFormula, is_atomic, is_conjunction, is_disjunction
from .visitors import FormulaVisitor, FormulaTransformationVisitor
from .pnf import remove_conditionals, push_negations, is_formula_quantifierless


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
    def visit_constant(self, formula: ConstantFormula):
        p = PredicateFormula('p', [])

        match formula.value:
            case PropConstant.verum:
                return ConnectiveFormula(BinaryConnective.disjunction, p, NegationFormula(p))

            case PropConstant.falsum:
                return ConnectiveFormula(BinaryConnective.conjunction, p, NegationFormula(p))


def remove_constants(formula: Formula) -> Formula:
    return RemoveConstantsVisitor().visit(formula)


class HasReachableConjunctionVisitor(FormulaVisitor):
    def generic_visit(self, formula: Formula):
        return False

    def visit_negation(self, formula: NegationFormula):
        return False

    def visit_connective(self, formula: ConnectiveFormula):
        match formula.conn:
            case BinaryConnective.disjunction:
                return self.visit(formula.a) or self.visit(formula.b)

            case BinaryConnective.conjunction:
                    return True

            case _:
                    return False

    def visit_quantifier(self, formula: QuantifierFormula):
        return self.visit(formula.sub)


def has_reachable_conjunction(formula: Formula):
    return HasReachableConjunctionVisitor().visit(formula)


class PullConjunctionVisitor(FormulaTransformationVisitor):
    def visit_connective(self, formula: ConnectiveFormula):
        a = self.visit(formula.a)

        if is_disjunction(formula) and is_conjunction(a):
            return ConnectiveFormula(
                BinaryConnective.conjunction,
                self.visit(ConnectiveFormula(BinaryConnective.disjunction, a.a, formula.b)),
                self.visit(ConnectiveFormula(BinaryConnective.disjunction, a.b, formula.b))
            )

        b = self.visit(formula.b)

        if is_disjunction(formula) and is_conjunction(b):
            return ConnectiveFormula(
                BinaryConnective.conjunction,
                self.visit(ConnectiveFormula(BinaryConnective.disjunction, formula.a, b.a)),
                self.visit(ConnectiveFormula(BinaryConnective.disjunction, formula.a, b.b))
            )

        return ConnectiveFormula(formula.conn, a, b)


def pull_conjunction(formula: Formula) -> Formula:
    return PullConjunctionVisitor().visit(formula)


# This is alg:cnf_and_dnf in the text
def to_cnf(formula: Formula):
    assert is_formula_quantifierless(formula)
    return pull_conjunction(push_negations(remove_conditionals(remove_constants(formula))))


# This is alg:perfect_cnf_and_dnf in the text
def function_to_cnf(fun: Callable[..., bool]):
    fun_params = inspect.signature(fun).parameters

    if len(fun_params) == 0:
        p = PredicateFormula('p', [])
        return ConnectiveFormula(
            BinaryConnective.disjunction if fun() else BinaryConnective.conjunction,
            p,
            NegationFormula(p)
        )

    for param in fun_params.values():
        assert all('a' <= c <= 'z' for c in param.name), \
            f'In order to become a valid predicate name, the parameter name {param.name} must consist only of small Latin characters.'

    # These names will generate valid formulas only when they consist of Latin letters
    predicates = [PredicateFormula(param.name, []) for param in fun_params.values()]
    disjuncts: list[Formula] = []

    for arg_tuple in itertools.product([False, True], repeat=len(fun_params)):
        if fun(*arg_tuple) is False:
            disjuncts.append(
                connect_formulas(
                    [NegationFormula(p) if arg else p for p, arg in zip(predicates, arg_tuple)],
                    BinaryConnective.disjunction
                )
            )

    if len(disjuncts) == 0:  # fun is vacuously true
        p = predicates[0]
        return ConnectiveFormula(BinaryConnective.disjunction, p, NegationFormula(p))

    return connect_formulas(disjuncts, BinaryConnective.conjunction)
