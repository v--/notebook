from ...support.names import new_var_name
from .terms import Abstraction, Application, Term, Variable
from .visitors import TermVisitor


def new_variable(old: Variable, context: set[Variable]) -> Variable:
    return Variable(new_var_name(old.name, set(map(str, context))))


class FreeVariableVisitor(TermVisitor[set[Variable]]):
    def visit_variable(self, term: Variable):
        return {term}

    def visit_application(self, term: Application):
        return self.visit(term.a) | self.visit(term.b)

    def visit_abstraction(self, term: Abstraction):
        return self.visit(term.sub) - {term.var}


def get_free_variables(term: Term) -> set[Variable]:
    return FreeVariableVisitor().visit(term)


class BoundVariableVisitor(TermVisitor[set[Variable]]):
    def visit_variable(self, term: Variable):
        return set()

    def visit_application(self, term: Application):
        return self.visit(term.a) | self.visit(term.b)

    def visit_abstraction(self, term: Abstraction):
        return self.visit(term.sub) | {term.var}


def get_bound_variables(term: Term) -> set[Variable]:
    return BoundVariableVisitor().visit(term)


def get_formula_variables(term: Term) -> set[Variable]:
    return get_free_variables(term) | get_bound_variables(term)
