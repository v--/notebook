from typing import Generic, TypeVar

from .formulas import (
    ConnectiveFormula,
    ConstantFormula,
    EqualityFormula,
    Formula,
    NegationFormula,
    PredicateFormula,
    QuantifierFormula,
)
from .terms import FunctionTerm, Term, Variable


T = TypeVar('T')


class TermVisitor(Generic[T]):
    def visit(self, term: Term) -> T:
        match term:
            case Variable():
                return self.visit_variable(term)

            case FunctionTerm():
                return self.visit_function(term)

    def visit_variable(self, term: Variable) -> T:
        return self.generic_visit(term)

    def visit_function(self, term: FunctionTerm) -> T:
        return self.generic_visit(term)

    def generic_visit(self, term: Term) -> T:
        raise NotImplementedError


class TermTransformationVisitor(TermVisitor[Term]):
    def visit_variable(self, term: Variable):
        return term

    def visit_function(self, term: FunctionTerm):
        return FunctionTerm(
            term.name,
            [self.visit(arg) for arg in term.arguments]
        )


class FormulaVisitor(Generic[T]):
    def visit(self, formula: Formula) -> T:
        match formula:
            case ConstantFormula():
                return self.visit_constant(formula)

            case EqualityFormula():
                return self.visit_equality(formula)

            case PredicateFormula():
                return self.visit_predicate(formula)

            case NegationFormula():
                return self.visit_negation(formula)

            case ConnectiveFormula():
                return self.visit_connective(formula)

            case QuantifierFormula():
                return self.visit_quantifier(formula)

    def visit_constant(self, formula: ConstantFormula) -> T:
        return self.generic_visit(formula)

    def visit_equality(self, formula: EqualityFormula) -> T:
        return self.generic_visit(formula)

    def visit_predicate(self, formula: PredicateFormula) -> T:
        return self.generic_visit(formula)

    def visit_negation(self, formula: NegationFormula) -> T:
        return self.generic_visit(formula)

    def visit_connective(self, formula: ConnectiveFormula) -> T:
        return self.generic_visit(formula)

    def visit_quantifier(self, formula: QuantifierFormula) -> T:
        return self.generic_visit(formula)

    def generic_visit(self, formula: Formula) -> T:
        raise NotImplementedError


class FormulaTransformationVisitor(FormulaVisitor[Formula]):
    def visit_constant(self, formula: ConstantFormula):
        return formula

    def visit_equality(self, formula: EqualityFormula):
        return formula

    def visit_predicate(self, formula: PredicateFormula):
        return formula

    def visit_negation(self, formula: NegationFormula):
        return NegationFormula(self.visit(formula.sub))

    def visit_connective(self, formula: ConnectiveFormula):
        return ConnectiveFormula(
            formula.conn,
            self.visit(formula.a),
            self.visit(formula.b)
        )

    def visit_quantifier(self, formula: QuantifierFormula):
        return QuantifierFormula(
            formula.quantifier,
            formula.variable,
            self.visit(formula.sub)
        )
