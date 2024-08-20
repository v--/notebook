from .terms import Abstraction, Application, LambdaTerm, Variable


class TermVisitor[T]:
    def visit(self, term: LambdaTerm) -> T:
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

    def generic_visit(self, term: LambdaTerm) -> T:
        raise NotImplementedError


class TermTransformationVisitor(TermVisitor[LambdaTerm]):
    def visit_variable(self, term: Variable) -> LambdaTerm:
        return term

    def visit_application(self, term: Application) -> LambdaTerm:
        return Application(self.visit(term.a), self.visit(term.b))

    def visit_abstraction(self, term: Abstraction) -> LambdaTerm:
        return Abstraction(term.var, self.visit(term.sub))
