from ...parsing.identifiers import new_latin_identifier
from .terms import Abstraction, Application, LambdaTerm, Variable
from .visitors import TermVisitor


def new_variable(context: frozenset[Variable]) -> Variable:
    return Variable(new_latin_identifier(frozenset(var.identifier for var in context)))


class FreeVariableVisitor(TermVisitor[frozenset[Variable]]):
    def visit_variable(self, term: Variable) -> frozenset[Variable]:
        return frozenset([term])

    def visit_application(self, term: Application) -> frozenset[Variable]:
        return self.visit(term.a) | self.visit(term.b)

    def visit_abstraction(self, term: Abstraction) -> frozenset[Variable]:
        return self.visit(term.sub) - {term.var}


def get_free_variables(term: LambdaTerm) -> frozenset[Variable]:
    return FreeVariableVisitor().visit(term)


class BoundVariableVisitor(TermVisitor[frozenset[Variable]]):
    def visit_variable(self, term: Variable) -> frozenset[Variable]:  # noqa: ARG002
        return frozenset()

    def visit_application(self, term: Application) -> frozenset[Variable]:
        return self.visit(term.a) | self.visit(term.b)

    def visit_abstraction(self, term: Abstraction) -> frozenset[Variable]:
        return self.visit(term.sub) | {term.var}


def get_bound_variables(term: LambdaTerm) -> frozenset[Variable]:
    return BoundVariableVisitor().visit(term)


def get_formula_variables(term: LambdaTerm) -> frozenset[Variable]:
    return get_free_variables(term) | get_bound_variables(term)
