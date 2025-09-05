from .terms import (
    Constant,
    TypedAbstraction,
    TypedApplication,
    TypedTerm,
    UntypedAbstraction,
    UntypedApplication,
    UntypedTerm,
    Variable,
)


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


class TermVisitor[T]:
    def visit(self, term: UntypedTerm | TypedTerm) -> T:
        match term:
            case Constant():
                return self.visit_constant(term)

            case Variable():
                return self.visit_variable(term)

            case UntypedApplication():
                return self.visit_untyped_application(term)

            case UntypedAbstraction():
                return self.visit_untyped_abstraction(term)

            case TypedApplication():
                return self.visit_typed_application(term)

            case TypedAbstraction():
                return self.visit_typed_abstraction(term)

    def visit_constant(self, term: Constant) -> T:
        return self.generic_visit(term)

    def visit_variable(self, term: Variable) -> T:
        return self.generic_visit(term)

    def visit_untyped_application(self, term: UntypedApplication) -> T:
        return self.visit_application(term)

    def visit_typed_application(self, term: TypedApplication) -> T:
        return self.visit_application(term)

    def visit_application(self, term: UntypedApplication | TypedApplication) -> T:
        return self.generic_visit(term)

    def visit_untyped_abstraction(self, term: UntypedAbstraction) -> T:
        return self.visit_abstraction(term)

    def visit_typed_abstraction(self, term: TypedAbstraction) -> T:
        return self.visit_abstraction(term)

    def visit_abstraction(self, term: UntypedAbstraction | TypedAbstraction) -> T:
        return self.generic_visit(term)

    def generic_visit(self, term: UntypedTerm | TypedTerm) -> T:
        raise NotImplementedError
