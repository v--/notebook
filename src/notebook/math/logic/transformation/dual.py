from dataclasses import dataclass
from enum import Flag, auto

from ..alphabet import BinaryConnective, PropConstant, Quantifier
from ..formulas import (
    ConnectiveFormula,
    ConstantFormula,
    Formula,
    FormulaTransformationVisitor,
    NegationFormula,
    PredicateApplication,
    QuantifierFormula,
    is_predicate_application,
)


class DualFormulaKind(Flag):
    LITERALS = auto()
    CONNECTIVES = auto()
    COMBINED = LITERALS | CONNECTIVES


@dataclass
class DualFormulaVisitor(FormulaTransformationVisitor):
    kind: DualFormulaKind

    def visit_logical_constant(self, formula: ConstantFormula) -> ConstantFormula:
        if DualFormulaKind.CONNECTIVES in self.kind:
            match formula.value:
                case PropConstant.VERUM:
                    return ConstantFormula(PropConstant.FALSUM)

                case PropConstant.FALSUM:
                    return ConstantFormula(PropConstant.VERUM)

        return formula


    def visit_predicate(self, formula: PredicateApplication) -> Formula:
        if DualFormulaKind.LITERALS in self.kind:
            return NegationFormula(formula)

        return formula

    def visit_negation(self, formula: NegationFormula) -> Formula:
        if DualFormulaKind.LITERALS in self.kind and is_predicate_application(formula.body):
            return formula.body

        return NegationFormula(self.visit(formula.body))

    def visit_connective(self, formula: ConnectiveFormula) -> ConnectiveFormula:
        left = self.visit(formula.left)
        right = self.visit(formula.right)

        if DualFormulaKind.CONNECTIVES not in self.kind:
            return ConnectiveFormula(formula.conn, left, right)

        match formula.conn:
            case BinaryConnective.CONJUNCTION:
                return ConnectiveFormula(BinaryConnective.DISJUNCTION, left, right)

            case BinaryConnective.DISJUNCTION:
                return ConnectiveFormula(BinaryConnective.CONJUNCTION, left, right)

            case BinaryConnective.CONDITIONAL:
                return ConnectiveFormula(BinaryConnective.CONDITIONAL, right, left)

            case BinaryConnective.BICONDITIONAL:
                return ConnectiveFormula(BinaryConnective.BICONDITIONAL, left, right)

    def visit_quantifier(self, formula: QuantifierFormula) -> QuantifierFormula:
        body = self.visit(formula.body)

        if DualFormulaKind.CONNECTIVES not in self.kind:
            return QuantifierFormula(formula.quantifier, formula.var, body)

        match formula.quantifier:
            case Quantifier.UNIVERSAL:
                return QuantifierFormula(Quantifier.EXISTENTIAL, formula.var, body)

            case Quantifier.EXISTENTIAL:
                return QuantifierFormula(Quantifier.UNIVERSAL, formula.var, body)


# This is alg:dual_propositional_formulas in the monograph
def to_dual_formula(formula: Formula, kind: DualFormulaKind) -> Formula:
    return DualFormulaVisitor(kind).visit(formula)
