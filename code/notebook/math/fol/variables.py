from ...support.names import new_var_name
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


def new_variable(old: Variable, context: set[Variable]) -> Variable:
    return Variable(new_var_name(old.name, set(map(str, context))))


class TermVariableVisitor(TermVisitor[set[Variable]]):
    def visit_variable(self, term: Variable) -> set[Variable]:
        return {term}

    def visit_function(self, term: FunctionTerm) -> set[Variable]:
        return {var for arg in term.arguments for var in self.visit(arg)}


def get_term_variables(term: Term) -> set[Variable]:
    return TermVariableVisitor().visit(term)


class FreeVariableVisitor(FormulaVisitor[set[Variable]]):
    def visit_equality(self, formula: EqualityFormula) -> set[Variable]:
        return get_term_variables(formula.a) | get_term_variables(formula.b)

    def visit_predicate(self, formula: PredicateFormula) -> set[Variable]:
        return {var for arg in formula.arguments for var in get_term_variables(arg)}

    def visit_negation(self, formula: NegationFormula) -> set[Variable]:
        return self.visit(formula.sub)

    def visit_connective(self, formula: ConnectiveFormula) -> set[Variable]:
        return self.visit(formula.a) | self.visit(formula.b)

    def visit_quantifier(self, formula: QuantifierFormula) -> set[Variable]:
        return self.visit(formula.sub) - {formula.variable}


def get_free_variables(formula: Formula) -> set[Variable]:
    return FreeVariableVisitor().visit(formula)


class BoundVariableVisitor(FormulaVisitor[set[Variable]]):
    def visit_equality(self, formula: EqualityFormula) -> set[Variable]:  # noqa: ARG002
        return set()

    def visit_predicate(self, formula: PredicateFormula) -> set[Variable]:  # noqa: ARG002
        return set()

    def visit_negation(self, formula: NegationFormula) -> set[Variable]:
        return self.visit(formula.sub)

    def visit_connective(self, formula: ConnectiveFormula) -> set[Variable]:
        return self.visit(formula.a) | self.visit(formula.b)

    def visit_quantifier(self, formula: QuantifierFormula) -> set[Variable]:
        return self.visit(formula.sub) | {formula.variable}


def get_bound_variables(formula: Formula) -> set[Variable]:
    return BoundVariableVisitor().visit(formula)

def get_formula_variables(formula: Formula) -> set[Variable]:
    return get_free_variables(formula) | get_bound_variables(formula)
