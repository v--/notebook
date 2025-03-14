from .schemas import (
    MixedAbstractionSchema,
    MixedApplicationSchema,
    MixedTermSchema,
    TermPlaceholder,
    TypedAbstractionSchema,
    TypedApplicationSchema,
    TypedTermSchema,
    UntypedAbstractionSchema,
    UntypedApplicationSchema,
    UntypedTermSchema,
    VariablePlaceholder,
)
from .terms import Constant


class TermSchemaVisitor[T]:
    def visit(self, schema: MixedTermSchema) -> T:
        match schema:
            case Constant():
                return self.visit_constant(schema)

            case VariablePlaceholder():
                return self.visit_variable_placeholder(schema)

            case TermPlaceholder():
                return self.visit_term_placeholder(schema)

            case MixedApplicationSchema():
                return self.visit_application(schema)

            case MixedAbstractionSchema():
                return self.visit_abstraction(schema)

    def visit_constant(self, schema: Constant) -> T:
        return self.generic_visit(schema)

    def visit_variable_placeholder(self, schema: VariablePlaceholder) -> T:
        return self.generic_visit(schema)

    def visit_term_placeholder(self, schema: TermPlaceholder) -> T:
        return self.generic_visit(schema)

    def visit_application(self, schema: MixedApplicationSchema) -> T:
        return self.generic_visit(schema)

    def visit_abstraction(self, schema: MixedAbstractionSchema) -> T:
        return self.generic_visit(schema)

    def generic_visit(self, schema: MixedTermSchema) -> T:
        raise NotImplementedError


class UntypedTermSchemaVisitor[T]:
    def visit(self, schema: UntypedTermSchema) -> T:
        match schema:
            case Constant():
                return self.visit_constant(schema)

            case VariablePlaceholder():
                return self.visit_variable_placeholder(schema)

            case TermPlaceholder():
                return self.visit_term_placeholder(schema)

            case UntypedApplicationSchema():
                return self.visit_application(schema)

            case UntypedAbstractionSchema():
                return self.visit_abstraction(schema)

    def visit_constant(self, schema: Constant) -> T:
        return self.generic_visit(schema)

    def visit_variable_placeholder(self, schema: VariablePlaceholder) -> T:
        return self.generic_visit(schema)

    def visit_term_placeholder(self, schema: TermPlaceholder) -> T:
        return self.generic_visit(schema)

    def visit_application(self, schema: UntypedApplicationSchema) -> T:
        return self.generic_visit(schema)

    def visit_abstraction(self, schema: UntypedAbstractionSchema) -> T:
        return self.generic_visit(schema)

    def generic_visit(self, schema: UntypedTermSchema) -> T:
        raise NotImplementedError


class TypedTermSchemaVisitor[T]:
    def visit(self, schema: TypedTermSchema) -> T:
        match schema:
            case Constant():
                return self.visit_constant(schema)

            case VariablePlaceholder():
                return self.visit_variable_placeholder(schema)

            case TermPlaceholder():
                return self.visit_term_placeholder(schema)

            case TypedApplicationSchema():
                return self.visit_application(schema)

            case TypedAbstractionSchema():
                return self.visit_abstraction(schema)

    def visit_constant(self, schema: Constant) -> T:
        return self.generic_visit(schema)

    def visit_variable_placeholder(self, schema: VariablePlaceholder) -> T:
        return self.generic_visit(schema)

    def visit_term_placeholder(self, schema: TermPlaceholder) -> T:
        return self.generic_visit(schema)

    def visit_application(self, schema: TypedApplicationSchema) -> T:
        return self.generic_visit(schema)

    def visit_abstraction(self, schema: TypedAbstractionSchema) -> T:
        return self.generic_visit(schema)

    def generic_visit(self, schema: TypedTermSchema) -> T:
        raise NotImplementedError
