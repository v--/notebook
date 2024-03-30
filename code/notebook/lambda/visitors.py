from typing import TypeVar, Generic

from .terms import Variable, Application, Abstraction, Term


T = TypeVar('T')


class TermVisitor(Generic[T]):
    def visit(self, term: Term) -> T:
        match term:
            case Variable():
                return self.visit_variable(term)

            case Application():
                return self.visit_application(term)

            case Abstraction():
                return self.visit_abstraction(term)

    def visit_variable(self, term: Variable) -> T:
        return self.generic_visit(term)

    def visit_application(self, term: Application) -> T:
        return self.generic_visit(term)

    def visit_abstraction(self, term: Abstraction) -> T:
        return self.generic_visit(term)

    def generic_visit(self, term: Term) -> T:
        raise NotImplementedError


class TermTransformationVisitor(TermVisitor[Term]):
    def visit_variable(self, term: Variable):
        return term

    def visit_application(self, term: Application):
        return Application(self.visit(term.a), self.visit(term.b))

    def visit_abstraction(self, term: Abstraction):
        return Application(term.var, self.visit(term.sub))
