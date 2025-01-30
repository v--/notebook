from typing import override

from .terms import (
    FunctionTerm,
    Term,
    Variable,
)


class TermVisitor[T]:
    def visit(self, term: Term) -> T:
        match term:
            case Variable():
                return self.visit_variable(term)

            case FunctionTerm():
                return self.visit_function(term)

    def visit_variable(self, term: Variable) -> T:
        return self.generic_visit(term)

    def visit_function(self, term: FunctionTerm) -> T:
        return self.generic_visit(term)

    def generic_visit(self, term: Term) -> T:
        raise NotImplementedError


class TermTransformationVisitor(TermVisitor[Term]):
    @override
    def visit_variable(self, term: Variable) -> Term:
        return term

    @override
    def visit_function(self, term: FunctionTerm) -> Term:
        return FunctionTerm(
            term.name,
            [self.visit(arg) for arg in term.arguments]
        )
