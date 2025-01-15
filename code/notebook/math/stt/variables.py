from collections.abc import Collection

from ...parsing.identifiers import new_latin_identifier
from .terms import Abstraction, Application, LambdaTerm, Variable
from .visitors import TermVisitor


def new_variable(context: Collection[Variable]) -> Variable:
    return Variable(new_latin_identifier({var.identifier for var in context}))


class FreeVariableVisitor(TermVisitor[Collection[Variable]]):
    def visit_variable(self, term: Variable) -> Collection[Variable]:
        return {term}

    def visit_application(self, term: Application) -> Collection[Variable]:
        return {*self.visit(term.a), *self.visit(term.b)}

    def visit_abstraction(self, term: Abstraction) -> Collection[Variable]:
        return {var for var in self.visit(term.sub) if var != term.var}


def get_free_variables(term: LambdaTerm) -> Collection[Variable]:
    return FreeVariableVisitor().visit(term)


class BoundVariableVisitor(TermVisitor[Collection[Variable]]):
    def visit_variable(self, term: Variable) -> Collection[Variable]:  # noqa: ARG002
        return set()

    def visit_application(self, term: Application) -> Collection[Variable]:
        return {*self.visit(term.a), *self.visit(term.b)}

    def visit_abstraction(self, term: Abstraction) -> Collection[Variable]:
        return {*self.visit(term.sub), term.var}


def get_bound_variables(term: LambdaTerm) -> Collection[Variable]:
    return BoundVariableVisitor().visit(term)


def get_formula_variables(term: LambdaTerm) -> Collection[Variable]:
    return {*get_free_variables(term), *get_bound_variables(term)}
