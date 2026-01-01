from dataclasses import dataclass
from typing import override

from ...alphabet import BinaryConnective, LatticeConnective, get_dual_connective
from ...formulas import (
    ConnectiveFormula,
    Formula,
    FormulaTransformationVisitor,
    NegationFormula,
    QuantifierFormula,
)
from ...propositional import PropFormula, convert_to_prop_formula
from ...transformation import dualize_formula
from ..exceptions import UnsupportedFormulaError


@dataclass
class FormulaToPolynomialFormVisitor(FormulaTransformationVisitor):
    inner: LatticeConnective

    @override
    def visit_negation(self, formula: NegationFormula) -> Formula:
        dual_visitor = FormulaToPolynomialFormVisitor(get_dual_connective(self.inner))
        return dualize_formula(dual_visitor.visit(formula.body))

    @override
    def visit_connective(self, formula: ConnectiveFormula) -> Formula:
        outer = get_dual_connective(self.inner)

        match formula.conn:
            case BinaryConnective.CONDITIONAL:
                return self.visit(
                    ConnectiveFormula(BinaryConnective.DISJUNCTION, NegationFormula(formula.left), formula.right)
                )

            case BinaryConnective.BICONDITIONAL:
                match self.inner:
                    case BinaryConnective.DISJUNCTION:
                        return self.visit(
                            ConnectiveFormula(BinaryConnective.CONJUNCTION,
                                ConnectiveFormula(BinaryConnective.DISJUNCTION, NegationFormula(formula.left), formula.right),
                                ConnectiveFormula(BinaryConnective.DISJUNCTION, formula.left, NegationFormula(formula.right))
                            )
                        )

                    case BinaryConnective.CONJUNCTION:
                        return self.visit(
                            ConnectiveFormula(BinaryConnective.DISJUNCTION,
                                ConnectiveFormula(BinaryConnective.CONJUNCTION, formula.left, formula.right),
                                ConnectiveFormula(BinaryConnective.CONJUNCTION, NegationFormula(formula.left), NegationFormula(formula.right))
                            )
                        )

            case _ if formula.conn == outer:
                left = self.visit(formula.left)
                right = self.visit(formula.right)
                return ConnectiveFormula(outer, left, right)

            case _:
                left = self.visit(formula.left)

                if isinstance(left, ConnectiveFormula) and left.conn == outer:
                    return ConnectiveFormula(
                        outer,
                        self.visit(ConnectiveFormula(self.inner, left.left, formula.right)),
                        self.visit(ConnectiveFormula(self.inner, left.right, formula.right)),
                    )

                right = self.visit(formula.right)

                if isinstance(right, ConnectiveFormula) and right.conn == outer:
                    return ConnectiveFormula(
                        outer,
                        self.visit(ConnectiveFormula(self.inner, left, right.left)),
                        self.visit(ConnectiveFormula(self.inner, left, right.right)),
                    )

                return ConnectiveFormula(self.inner, left, right)

    @override
    def visit_quantifier(self, formula: QuantifierFormula) -> Formula:
        raise UnsupportedFormulaError('We only allow quantifier-free formulas to be converted to conjunctive normal form')


def formula_to_polynomial_form(formula: Formula, inner: LatticeConnective) -> Formula:
    return FormulaToPolynomialFormVisitor(inner).visit(formula)


def formula_to_cnf(formula: Formula) -> Formula:
    return formula_to_polynomial_form(formula, inner=BinaryConnective.DISJUNCTION)


# This is alg:formula_to_cnf in the monograph
def formula_to_cnf_prop(formula: PropFormula) -> PropFormula:
    return convert_to_prop_formula(formula_to_cnf(formula))


def formula_to_dnf(formula: Formula) -> Formula:
    return formula_to_polynomial_form(formula, inner=BinaryConnective.CONJUNCTION)


def formula_to_dnf_prop(formula: PropFormula) -> PropFormula:
    return convert_to_prop_formula(formula_to_dnf(formula))
