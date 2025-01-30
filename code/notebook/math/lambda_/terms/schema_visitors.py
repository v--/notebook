from .schemas import AbstractionSchema, ApplicationSchema, TermPlaceholder, TermSchema, VariablePlaceholder
from .terms import Constant


class TermSchemaVisitor[T]:
    def visit(self, schema: TermSchema) -> T:
        match schema:
            case Constant():
                return self.visit_constant(schema)

            case VariablePlaceholder():
                return self.visit_variable_placeholder(schema)

            case ApplicationSchema():
                return self.visit_application(schema)

            case AbstractionSchema():
                return self.visit_abstraction(schema)

            case TermPlaceholder():
                return self.visit_term_placeholder(schema)

    def visit_constant(self, schema: Constant) -> T:
        return self.generic_visit(schema)

    def visit_variable_placeholder(self, schema: VariablePlaceholder) -> T:
        return self.generic_visit(schema)

    def visit_term_placeholder(self, schema: TermPlaceholder) -> T:
        return self.generic_visit(schema)

    def visit_application(self, schema: ApplicationSchema) -> T:
        return self.generic_visit(schema)

    def visit_abstraction(self, schema: AbstractionSchema) -> T:
        return self.generic_visit(schema)

    def generic_visit(self, schema: TermSchema) -> T:
        raise NotImplementedError
