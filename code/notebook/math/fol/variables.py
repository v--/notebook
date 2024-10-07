from collections.abc import Collection

from ...parsing.identifiers import new_latin_identifier
from .formulas import (
    ConnectiveFormula,
    EqualityFormula,
    Formula,
    NegationFormula,
    PredicateFormula,
    QuantifierFormula,
)
from .parsing import parse_variable
from .terms import FunctionTerm, Term, Variable
from .visitors import FormulaVisitor, TermVisitor


class common:  # noqa: N801
    x = parse_variable('x')
    y = parse_variable('y')
    z = parse_variable('z')


def new_variable(context: Collection[Variable]) -> Variable:
    return Variable(new_latin_identifier({var.identifier for var in context}))


class TermVariableVisitor(TermVisitor[Collection[Variable]]):
    def visit_variable(self, term: Variable) -> Collection[Variable]:
        return {term}

    def visit_function(self, term: FunctionTerm) -> Collection[Variable]:
        return {var for arg in term.arguments for var in self.visit(arg)}


def get_term_variables(term: Term) -> Collection[Variable]:
    return TermVariableVisitor().visit(term)


class FreeVariableVisitor(FormulaVisitor[Collection[Variable]]):
    def visit_equality(self, formula: EqualityFormula) -> Collection[Variable]:
        return {*get_term_variables(formula.a), *get_term_variables(formula.b)}

    def visit_predicate(self, formula: PredicateFormula) -> Collection[Variable]:
        return {var for arg in formula.arguments for var in get_term_variables(arg)}

    def visit_negation(self, formula: NegationFormula) -> Collection[Variable]:
        return self.visit(formula.sub)

    def visit_connective(self, formula: ConnectiveFormula) -> Collection[Variable]:
        return {*self.visit(formula.a), *self.visit(formula.b)}

    def visit_quantifier(self, formula: QuantifierFormula) -> Collection[Variable]:
        return {var for var in self.visit(formula.sub) if var != formula.variable}


def get_free_variables(formula: Formula) -> Collection[Variable]:
    return FreeVariableVisitor().visit(formula)


class BoundVariableVisitor(FormulaVisitor[Collection[Variable]]):
    def visit_equality(self, formula: EqualityFormula) -> Collection[Variable]:  # noqa: ARG002
        return set()

    def visit_predicate(self, formula: PredicateFormula) -> Collection[Variable]:  # noqa: ARG002
        return set()

    def visit_negation(self, formula: NegationFormula) -> Collection[Variable]:
        return self.visit(formula.sub)

    def visit_connective(self, formula: ConnectiveFormula) -> Collection[Variable]:
        return {*self.visit(formula.a), *self.visit(formula.b)}

    def visit_quantifier(self, formula: QuantifierFormula) -> Collection[Variable]:
        return {*self.visit(formula.sub), formula.variable}


def get_bound_variables(formula: Formula) -> Collection[Variable]:
    return BoundVariableVisitor().visit(formula)

def get_formula_variables(formula: Formula) -> Collection[Variable]:
    return {*get_free_variables(formula), *get_bound_variables(formula)}
