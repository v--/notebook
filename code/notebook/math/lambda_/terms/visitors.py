from .terms import Abstraction, Application, Constant, Term, Variable


class TermVisitor[T]:
    def visit(self, term: Term) -> T:
        match term:
            case Constant():
                return self.visit_constant(term)

            case Variable():
                return self.visit_variable(term)

            case Application():
                return self.visit_application(term)

            case Abstraction():
                return self.visit_abstraction(term)

    def visit_constant(self, term: Constant) -> T:
        return self.generic_visit(term)

    def visit_variable(self, term: Variable) -> T:
        return self.generic_visit(term)

    def visit_application(self, term: Application) -> T:
        return self.generic_visit(term)

    def visit_abstraction(self, term: Abstraction) -> T:
        return self.generic_visit(term)

    def generic_visit(self, term: Term) -> T:
        raise NotImplementedError


class TermTransformationVisitor(TermVisitor[Term]):
    def visit_constant(self, term: Constant) -> Term:
        return term

    def visit_variable(self, term: Variable) -> Term:
        return term

    def visit_application(self, term: Application) -> Term:
        return Application(self.visit(term.a), self.visit(term.b))

    def visit_abstraction(self, term: Abstraction) -> Term:
        return Abstraction(term.var, self.visit(term.sub))
