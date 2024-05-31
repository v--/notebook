from ...parsing.identifiers import new_latin_identifier
from .formulas import (
    ConnectiveFormula,
    EqualityFormula,
    Formula,
    NegationFormula,
    PredicateFormula,
    QuantifierFormula,
)
from .terms import FunctionTerm, Term, Variable
from .visitors import FormulaVisitor, TermVisitor


def new_variable(context: frozenset[Variable]) -> Variable:
    return Variable(new_latin_identifier(frozenset(var.identifier for var in context)))


class TermVariableVisitor(TermVisitor[frozenset[Variable]]):
    def visit_variable(self, term: Variable) -> frozenset[Variable]:
        return frozenset([term])

    def visit_function(self, term: FunctionTerm) -> frozenset[Variable]:
        return frozenset(var for arg in term.arguments for var in self.visit(arg))


def get_term_variables(term: Term) -> frozenset[Variable]:
    return TermVariableVisitor().visit(term)


class FreeVariableVisitor(FormulaVisitor[frozenset[Variable]]):
    def visit_equality(self, formula: EqualityFormula) -> frozenset[Variable]:
        return get_term_variables(formula.a) | get_term_variables(formula.b)

    def visit_predicate(self, formula: PredicateFormula) -> frozenset[Variable]:
        return frozenset(var for arg in formula.arguments for var in get_term_variables(arg))

    def visit_negation(self, formula: NegationFormula) -> frozenset[Variable]:
        return self.visit(formula.sub)

    def visit_connective(self, formula: ConnectiveFormula) -> frozenset[Variable]:
        return self.visit(formula.a) | self.visit(formula.b)

    def visit_quantifier(self, formula: QuantifierFormula) -> frozenset[Variable]:
        return self.visit(formula.sub) - {formula.variable}


def get_free_variables(formula: Formula) -> frozenset[Variable]:
    return FreeVariableVisitor().visit(formula)


class BoundVariableVisitor(FormulaVisitor[frozenset[Variable]]):
    def visit_equality(self, formula: EqualityFormula) -> frozenset[Variable]:  # noqa: ARG002
        return frozenset()

    def visit_predicate(self, formula: PredicateFormula) -> frozenset[Variable]:  # noqa: ARG002
        return frozenset()

    def visit_negation(self, formula: NegationFormula) -> frozenset[Variable]:
        return self.visit(formula.sub)

    def visit_connective(self, formula: ConnectiveFormula) -> frozenset[Variable]:
        return self.visit(formula.a) | self.visit(formula.b)

    def visit_quantifier(self, formula: QuantifierFormula) -> frozenset[Variable]:
        return self.visit(formula.sub) | {formula.variable}


def get_bound_variables(formula: Formula) -> frozenset[Variable]:
    return BoundVariableVisitor().visit(formula)

def get_formula_variables(formula: Formula) -> frozenset[Variable]:
    return get_free_variables(formula) | get_bound_variables(formula)
