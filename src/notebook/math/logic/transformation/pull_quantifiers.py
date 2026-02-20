from typing import override

from ..alphabet import BinaryConnective, get_dual_quantifier
from ..formulas import (
    ConnectiveFormula,
    Formula,
    FormulaTransformationVisitor,
    NegationFormula,
    QuantifierFormula,
)
from ..substitution import substitute_in_formula
from ..variables import get_formula_free_variables, new_variable
from .collapse_repeated_negation import collapse_repeated_negation


class PullQuantifiersVisitor(FormulaTransformationVisitor):
    @override
    def visit_negation(self, formula: NegationFormula) -> Formula:
        body = self.visit(formula.body)

        if isinstance(body, QuantifierFormula):
            return QuantifierFormula(
                get_dual_quantifier(body.quant),
                body.var,
                collapse_repeated_negation(self.visit(NegationFormula(body.body)))
            )

        return NegationFormula(body)

    @override
    def visit_connective(self, formula: ConnectiveFormula) -> Formula:
        left = self.visit(formula.left)
        right = self.visit(formula.right)

        if formula.conn == BinaryConnective.BICONDITIONAL and (isinstance(left, QuantifierFormula) or isinstance(right, QuantifierFormula)):
            return self.visit(
                ConnectiveFormula(
                    BinaryConnective.CONJUNCTION,
                    ConnectiveFormula(BinaryConnective.CONDITIONAL, left, right),
                    ConnectiveFormula(BinaryConnective.CONDITIONAL, right, left)
                )
            )

        if isinstance(left, QuantifierFormula):
            right_free = get_formula_free_variables(right)

            if left.var in right_free:
                left_new_var = new_variable({*get_formula_free_variables(left), *right_free})
            else:
                left_new_var = left.var

            body = self.visit(
                ConnectiveFormula(
                    formula.conn,
                    substitute_in_formula(left.body, {left.var: left_new_var}),
                    right,
                )
            )

            match formula.conn:
                case BinaryConnective.CONJUNCTION | BinaryConnective.DISJUNCTION:
                    return QuantifierFormula(left.quant, left_new_var, body)

                case BinaryConnective.CONDITIONAL:
                    return QuantifierFormula(get_dual_quantifier(left.quant), left_new_var, body)

        if isinstance(right, QuantifierFormula):
            left_free = get_formula_free_variables(left)

            if right.var in left_free:
                right_new_var = new_variable({*get_formula_free_variables(right), *left_free})
            else:
                right_new_var = right.var

            body = self.visit(
                ConnectiveFormula(
                    formula.conn,
                    left,
                    substitute_in_formula(right.body, {right.var: right_new_var}),
                )
            )

            return QuantifierFormula(right.quant, right_new_var, body)

        return ConnectiveFormula(formula.conn, left, right)


def pull_quantifiers(formula: Formula) -> Formula:
    return PullQuantifiersVisitor().visit(formula)
