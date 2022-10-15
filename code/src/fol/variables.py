from .types import FunctionTerm, Formula, EqualityFormula, PredicateFormula, NegationFormula, ConnectiveFormula, QuantifierFormula, Formula, Term, Variable
from .visitors import FormulaVisitor, TermVisitor


class TermVariableVisitor(TermVisitor):
    def visit_variable(self, term: Variable):
        return {term.name}

    def visit_function(self, term: FunctionTerm):
        return {var for arg in term.arguments for var in self.visit(arg)}


def get_variables(term: Term) -> set[str]:
    return TermVariableVisitor().visit(term)


class FreeVariableVisitor(FormulaVisitor):
    def visit_equality(self, formula: EqualityFormula):
        return get_variables(formula.a) | get_variables(formula.b)

    def visit_predicate(self, formula: PredicateFormula):
        return {var for arg in formula.arguments for var in get_variables(arg)}

    def visit_negation(self, formula: NegationFormula):
        return self.visit(formula.sub)

    def visit_connective(self, formula: ConnectiveFormula):
        return self.visit(formula.a) | self.visit(formula.b)

    def visit_quantifier(self, formula: QuantifierFormula):
        return self.visit(formula.sub) - {formula.variable.name}


def get_free_variables(formula: Formula) -> set[str]:
    return FreeVariableVisitor().visit(formula)


class BoundVariableVisitor(FormulaVisitor):
    def visit_equality(self, formula: EqualityFormula):
        return set()

    def visit_predicate(self, formula: PredicateFormula):
        return set()

    def visit_negation(self, formula: NegationFormula):
        return self.visit(formula.sub)

    def visit_connective(self, formula: ConnectiveFormula):
        return self.visit(formula.a) | self.visit(formula.b)

    def visit_quantifier(self, formula: QuantifierFormula):
        return self.visit(formula.sub) | {formula.variable.name}


def get_bound_variables(formula: Formula) -> set[str]:
    return BoundVariableVisitor().visit(formula)
