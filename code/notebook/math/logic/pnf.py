from typing import override

from ...exceptions import NotebookCodeError
from .alphabet import BinaryConnective, Quantifier
from .formulas import (
    ConnectiveFormula,
    Formula,
    FormulaTransformationVisitor,
    FormulaVisitor,
    NegationFormula,
    QuantifierFormula,
)
from .substitution import substitute_in_formula
from .variables import get_bound_variables, get_free_variables, new_variable


class PNFError(NotebookCodeError):
    pass


class QuantifierlessVerificationVisitor(FormulaVisitor[bool]):
    @override
    def generic_visit(self, formula: Formula) -> bool:
        return True

    @override
    def visit_negation(self, formula: NegationFormula) -> bool:
        return self.visit(formula.body)

    @override
    def visit_connective(self, formula: ConnectiveFormula) -> bool:
        return self.visit(formula.left) and self.visit(formula.right)

    @override
    def visit_quantifier(self, formula: QuantifierFormula) -> bool:
        return False


def is_formula_quantifierless(formula: Formula) -> bool:
    return QuantifierlessVerificationVisitor().visit(formula)


class PNFVerificationVisitor(FormulaVisitor[bool]):
    @override
    def generic_visit(self, formula: Formula) -> bool:
        return True

    @override
    def visit_negation(self, formula: NegationFormula) -> bool:
        if isinstance(formula.body, QuantifierFormula):
            return False

        return self.visit(formula.body)

    @override
    def visit_connective(self, formula: ConnectiveFormula) -> bool:
        if isinstance(formula.left, QuantifierFormula) or isinstance(formula.right, QuantifierFormula):
            return False

        return self.visit(formula.left) and self.visit(formula.right)

    @override
    def visit_quantifier(self, formula: QuantifierFormula) -> bool:
        return self.visit(formula.body)


def is_formula_in_pnf(formula: Formula) -> bool:
    return PNFVerificationVisitor().visit(formula)


class ConditionalRemovalVisitor(FormulaTransformationVisitor):
    @override
    def visit_connective(self, formula: ConnectiveFormula) -> ConnectiveFormula:
        a = self.visit(formula.left)
        b = self.visit(formula.right)

        match formula.conn:
            case BinaryConnective.DISJUNCTION | BinaryConnective.CONJUNCTION:
                return ConnectiveFormula(formula.conn, a, b)

            case BinaryConnective.CONDITIONAL:
                return ConnectiveFormula(BinaryConnective.DISJUNCTION, NegationFormula(a), b)

            case BinaryConnective.BICONDITIONAL:
                return ConnectiveFormula(
                    BinaryConnective.CONJUNCTION,
                    ConnectiveFormula(BinaryConnective.DISJUNCTION, NegationFormula(a), b),
                    ConnectiveFormula(BinaryConnective.DISJUNCTION, a, NegationFormula(b))
                )


def remove_conditionals(formula: Formula) -> Formula:
    return ConditionalRemovalVisitor().visit(formula)


class MoveNegationsVisitor(FormulaTransformationVisitor):
    @override
    def visit_negation(self, formula: NegationFormula) -> Formula:
        if isinstance(formula.body, ConnectiveFormula):
            new_conn: BinaryConnective

            match formula.body.conn:
                case BinaryConnective.DISJUNCTION:
                    new_conn = BinaryConnective.CONJUNCTION
                case BinaryConnective.CONJUNCTION:
                    new_conn = BinaryConnective.DISJUNCTION
                case _:
                    raise PNFError(f'Unexpected connective {formula.body.conn}')

            return ConnectiveFormula(
                new_conn,
                self.visit(NegationFormula(formula.body.left)),
                self.visit(NegationFormula(formula.body.right))
            )

        if isinstance(formula.body, QuantifierFormula):
            new_quantifier: Quantifier

            match formula.body.quantifier:
                case Quantifier.UNIVERSAL:
                    new_quantifier = Quantifier.EXISTENTIAL
                case Quantifier.EXISTENTIAL:
                    new_quantifier = Quantifier.UNIVERSAL
                case _:
                    raise PNFError(f'Unexpected quantifier {formula.body.quantifier}')

            return QuantifierFormula(
                new_quantifier,
                formula.body.var,
                self.visit(NegationFormula(formula.body.body))
            )

        if isinstance(formula.body, NegationFormula):
            return self.visit(formula.body.body)

        return NegationFormula(self.visit(formula.body))

    @override
    def visit_connective(self, formula: ConnectiveFormula) -> Formula:
        if formula.conn not in (BinaryConnective.DISJUNCTION, BinaryConnective.CONJUNCTION):
            raise PNFError(f'Unexpected connective {formula.conn}')

        return super().visit_connective(formula)


def move_negations(formula: Formula) -> Formula:
    return MoveNegationsVisitor().visit(formula)


class MoveQuantifiersVisitor(FormulaTransformationVisitor):
    @override
    def visit_connective(self, formula: ConnectiveFormula) -> Formula:
        if formula.conn not in (BinaryConnective.DISJUNCTION, BinaryConnective.CONJUNCTION):
            raise PNFError(f'Unexpected connective {formula.conn}')

        if isinstance(formula.left, QuantifierFormula):
            new_var = new_variable({*get_free_variables(formula.left.body), *get_free_variables(formula.right)})

            return QuantifierFormula(
                formula.left.quantifier,
                new_var,
                self.visit(
                    ConnectiveFormula(
                        formula.conn,
                        substitute_in_formula(formula.left.body, formula.left.var, new_var),
                        formula.right
                    )
                )
            )

        if isinstance(formula.right, QuantifierFormula):
            new_var = new_variable({*get_free_variables(formula.left), *get_free_variables(formula.right.body)})

            return QuantifierFormula(
                formula.right.quantifier,
                new_var,
                self.visit(
                    ConnectiveFormula(
                        formula.conn,
                        formula.left,
                        substitute_in_formula(formula.right.body, formula.right.var, new_var),
                    )
                )
            )

        if len(get_bound_variables(formula.left)) == 0 and len(get_bound_variables(formula.right)) == 0:
            return formula

        return self.visit(
            ConnectiveFormula(
                formula.conn,
                self.visit(formula.left),
                self.visit(formula.right)
            )
        )


def move_quantifiers(formula: Formula) -> Formula:
    return MoveQuantifiersVisitor().visit(formula)


# This is alg:prenex_normal_form_conversion in the monograph
def to_pnf(formula: Formula) -> Formula:
    return move_quantifiers(move_negations(remove_conditionals(formula)))
