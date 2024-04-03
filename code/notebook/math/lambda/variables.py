from ...support.names import new_var_name
from .terms import Abstraction, Application, LambdaTerm, Variable
from .visitors import TermVisitor


def new_variable(old: Variable, context: set[Variable]) -> Variable:
    return Variable(new_var_name(old.name, set(map(str, context))))


class FreeVariableVisitor(TermVisitor[set[Variable]]):
    def visit_variable(self, term: Variable) -> set[Variable]:
        return {term}

    def visit_application(self, term: Application) -> set[Variable]:
        return self.visit(term.a) | self.visit(term.b)

    def visit_abstraction(self, term: Abstraction) -> set[Variable]:
        return self.visit(term.sub) - {term.var}


def get_free_variables(term: LambdaTerm) -> set[Variable]:
    return FreeVariableVisitor().visit(term)


class BoundVariableVisitor(TermVisitor[set[Variable]]):
    def visit_variable(self, term: Variable) -> set[Variable]:  # noqa: ARG002
        return set()

    def visit_application(self, term: Application) -> set[Variable]:
        return self.visit(term.a) | self.visit(term.b)

    def visit_abstraction(self, term: Abstraction) -> set[Variable]:
        return self.visit(term.sub) | {term.var}


def get_bound_variables(term: LambdaTerm) -> set[Variable]:
    return BoundVariableVisitor().visit(term)


def get_formula_variables(term: LambdaTerm) -> set[Variable]:
    return get_free_variables(term) | get_bound_variables(term)
