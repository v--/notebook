from .terms import (
    Constant,
    MixedAbstraction,
    MixedApplication,
    MixedTerm,
    TypedAbstraction,
    TypedApplication,
    TypedTerm,
    UntypedAbstraction,
    UntypedApplication,
    UntypedTerm,
    Variable,
)


class TermVisitor[T]:
    def visit(self, term: MixedTerm) -> T:
        match term:
            case Constant():
                return self.visit_constant(term)

            case Variable():
                return self.visit_variable(term)

            case MixedApplication():
                return self.visit_application(term)

            case MixedAbstraction():
                return self.visit_abstraction(term)

    def visit_constant(self, term: Constant) -> T:
        return self.generic_visit(term)


    def visit_variable(self, term: Variable) -> T:
        return self.generic_visit(term)

    def visit_application(self, term: MixedApplication) -> T:
        return self.generic_visit(term)

    def visit_abstraction(self, term: MixedAbstraction) -> T:
        return self.generic_visit(term)

    def generic_visit(self, term: MixedTerm) -> T:
        raise NotImplementedError


class UntypedTermVisitor[T]:
    def visit(self, term: UntypedTerm) -> T:
        match term:
            case Constant():
                return self.visit_constant(term)

            case Variable():
                return self.visit_variable(term)

            case UntypedApplication():
                return self.visit_application(term)

            case UntypedAbstraction():
                return self.visit_abstraction(term)

    def visit_constant(self, term: Constant) -> T:
        return self.generic_visit(term)

    def visit_variable(self, term: Variable) -> T:
        return self.generic_visit(term)

    def visit_application(self, term: UntypedApplication) -> T:
        return self.generic_visit(term)

    def visit_abstraction(self, term: UntypedAbstraction) -> T:
        return self.generic_visit(term)

    def generic_visit(self, term: UntypedTerm) -> T:
        raise NotImplementedError


class TypedTermVisitor[T]:
    def visit(self, term: TypedTerm) -> T:
        match term:
            case Constant():
                return self.visit_constant(term)

            case Variable():
                return self.visit_variable(term)

            case TypedApplication():
                return self.visit_application(term)

            case TypedAbstraction():
                return self.visit_abstraction(term)

    def visit_constant(self, term: Constant) -> T:
        return self.generic_visit(term)

    def visit_variable(self, term: Variable) -> T:
        return self.generic_visit(term)

    def visit_application(self, term: TypedApplication) -> T:
        return self.generic_visit(term)

    def visit_abstraction(self, term: TypedAbstraction) -> T:
        return self.generic_visit(term)

    def generic_visit(self, term: TypedTerm) -> T:
        raise NotImplementedError
