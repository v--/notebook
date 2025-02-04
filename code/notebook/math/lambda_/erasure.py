from typing import override

from .terms import (
    Constant,
    TypedAbstraction,
    TypedApplication,
    TypedTerm,
    TypedTermVisitor,
    UntypedAbstraction,
    UntypedApplication,
    UntypedTerm,
    Variable,
)


class TypeErasureVisitor(TypedTermVisitor[UntypedTerm]):
    @override
    def visit_constant(self, term: Constant) -> Constant:
        return term

    @override
    def visit_variable(self, term: Variable) -> Variable:
        return term

    @override
    def visit_application(self, term: TypedApplication) -> UntypedApplication:
        return UntypedApplication(self.visit(term.a), self.visit(term.b))

    @override
    def visit_abstraction(self, term: TypedAbstraction) -> UntypedAbstraction:
        return UntypedAbstraction(term.var, self.visit(term.sub))



def erase_annotations(term: TypedTerm) -> UntypedTerm:
    return TypeErasureVisitor().visit(term)
