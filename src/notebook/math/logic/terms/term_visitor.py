from typing import override

from .terms import FunctionApplication, Term, Variable


class TermVisitor[T]:
    def visit(self, term: Term) -> T:
        match term:
            case Variable():
                return self.visit_variable(term)

            case FunctionApplication():
                return self.visit_function(term)

    def visit_variable(self, term: Variable) -> T:
        return self.generic_visit(term)

    def visit_function(self, term: FunctionApplication) -> T:
        return self.generic_visit(term)

    def generic_visit(self, term: Term) -> T:
        raise NotImplementedError


class TermTransformationVisitor(TermVisitor[Term]):
    @override
    def visit_variable(self, term: Variable) -> Term:
        return term

    @override
    def visit_function(self, term: FunctionApplication) -> Term:
        return FunctionApplication(
            term.name,
            [self.visit(arg) for arg in term.arguments]
        )
