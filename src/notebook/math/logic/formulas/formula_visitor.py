from typing import override

from ..alphabet import BinaryConnective, PropConstantSymbol, Quantifier
from .formulas import (
    AtomicFormula,
    ConnectiveFormula,
    EqualityFormula,
    Formula,
    NegationFormula,
    PredicateApplication,
    PropConstant,
    QuantifierFormula,
)


class FormulaVisitor[T]:
    def visit(self, formula: Formula) -> T:  # noqa: PLR0911
        match formula:
            case PropConstant():
                match formula.value:
                    case PropConstantSymbol.VERUM:
                        return self.visit_verum(formula)

                    case PropConstantSymbol.FALSUM:
                        return self.visit_falsum(formula)

            case EqualityFormula():
                return self.visit_equality(formula)

            case PredicateApplication():
                return self.visit_predicate(formula)

            case NegationFormula():
                return self.visit_negation(formula)

            case ConnectiveFormula():
                match formula.conn:
                    case BinaryConnective.CONJUNCTION:
                        return self.visit_conjunction(formula)

                    case BinaryConnective.DISJUNCTION:
                        return self.visit_disjunction(formula)

                    case BinaryConnective.CONDITIONAL:
                        return self.visit_conditional(formula)

                    case BinaryConnective.BICONDITIONAL:
                        return self.visit_biconditional(formula)

            case QuantifierFormula():
                match formula.quant:
                    case Quantifier.UNIVERSAL:
                        return self.visit_universal(formula)

                    case Quantifier.EXISTENTIAL:
                        return self.visit_existential(formula)

    def visit_atomic(self, formula: AtomicFormula) -> T:
        return self.generic_visit(formula)

    def visit_prop_constant(self, formula: PropConstant) -> T:
        return self.visit_atomic(formula)

    def visit_verum(self, formula: PropConstant) -> T:
        return self.visit_prop_constant(formula)

    def visit_falsum(self, formula: PropConstant) -> T:
        return self.visit_prop_constant(formula)

    def visit_equality(self, formula: EqualityFormula) -> T:
        return self.visit_atomic(formula)

    def visit_predicate(self, formula: PredicateApplication) -> T:
        return self.visit_atomic(formula)

    def visit_negation(self, formula: NegationFormula) -> T:
        return self.generic_visit(formula)

    def visit_connective(self, formula: ConnectiveFormula) -> T:
        return self.generic_visit(formula)

    def visit_conjunction(self, formula: ConnectiveFormula) -> T:
        return self.visit_connective(formula)

    def visit_disjunction(self, formula: ConnectiveFormula) -> T:
        return self.visit_connective(formula)

    def visit_conditional(self, formula: ConnectiveFormula) -> T:
        return self.visit_connective(formula)

    def visit_biconditional(self, formula: ConnectiveFormula) -> T:
        return self.visit_connective(formula)

    def visit_quantifier(self, formula: QuantifierFormula) -> T:
        return self.generic_visit(formula)

    def visit_universal(self, formula: QuantifierFormula) -> T:
        return self.visit_quantifier(formula)

    def visit_existential(self, formula: QuantifierFormula) -> T:
        return self.visit_quantifier(formula)

    def generic_visit(self, formula: Formula) -> T:
        raise NotImplementedError


class FormulaTransformationVisitor(FormulaVisitor[Formula]):
    @override
    def visit_atomic(self, formula: PropConstant | EqualityFormula | PredicateApplication) -> Formula:
        return formula

    @override
    def visit_negation(self, formula: NegationFormula) -> Formula:
        return NegationFormula(self.visit(formula.body))

    @override
    def visit_connective(self, formula: ConnectiveFormula) -> Formula:
        return ConnectiveFormula(
            formula.conn,
            self.visit(formula.left),
            self.visit(formula.right)
        )

    @override
    def visit_quantifier(self, formula: QuantifierFormula) -> Formula:
        return QuantifierFormula(
            formula.quant,
            formula.var,
            self.visit(formula.body)
        )
