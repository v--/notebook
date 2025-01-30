from collections.abc import Collection
from typing import override

from ...parsing.identifiers import new_latin_identifier
from .terms import Abstraction, Application, Constant, Term, TermVisitor, Variable


def new_variable(context: Collection[Variable]) -> Variable:
    return Variable(new_latin_identifier({var.identifier for var in context}))


class FreeVariableVisitor(TermVisitor[Collection[Variable]]):
    @override
    def visit_constant(self, term: Constant) -> Collection[Variable]:
        return set()

    @override
    def visit_variable(self, term: Variable) -> Collection[Variable]:
        return {term}

    @override
    def visit_application(self, term: Application) -> Collection[Variable]:
        return {*self.visit(term.a), *self.visit(term.b)}

    @override
    def visit_abstraction(self, term: Abstraction) -> Collection[Variable]:
        return {var for var in self.visit(term.sub) if var != term.var}


def get_free_variables(term: Term) -> Collection[Variable]:
    return FreeVariableVisitor().visit(term)


class BoundVariableVisitor(TermVisitor[Collection[Variable]]):
    @override
    def visit_constant(self, term: Constant) -> Collection[Variable]:
        return set()

    @override
    def visit_variable(self, term: Variable) -> Collection[Variable]:
        return set()

    @override
    def visit_application(self, term: Application) -> Collection[Variable]:
        return {*self.visit(term.a), *self.visit(term.b)}

    @override
    def visit_abstraction(self, term: Abstraction) -> Collection[Variable]:
        return {*self.visit(term.sub), term.var}


def get_bound_variables(term: Term) -> Collection[Variable]:
    return BoundVariableVisitor().visit(term)


def get_formula_variables(term: Term) -> Collection[Variable]:
    return {*get_free_variables(term), *get_bound_variables(term)}
