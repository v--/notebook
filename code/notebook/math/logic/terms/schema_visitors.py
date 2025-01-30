from .schemas import (
    ExtendedTermSchema,
    FunctionTermSchema,
    StarredTermSchema,
    TermPlaceholder,
    VariablePlaceholder,
)


class TermSchemaVisitor[T]:
    def visit(self, schema: ExtendedTermSchema) -> T:
        match schema:
            case VariablePlaceholder():
                return self.visit_variable_placeholder(schema)

            case TermPlaceholder():
                return self.visit_term_placeholder(schema)

            case FunctionTermSchema():
                return self.visit_function(schema)

            case StarredTermSchema():
                return self.visit_starred_schema(schema)

    def visit_variable_placeholder(self, schema: VariablePlaceholder) -> T:
        return self.generic_visit(schema)

    def visit_term_placeholder(self, schema: TermPlaceholder) -> T:
        return self.generic_visit(schema)

    def visit_function(self, schema: FunctionTermSchema) -> T:
        return self.generic_visit(schema)

    def visit_starred_schema(self, schema: StarredTermSchema) -> T:
        return self.generic_visit(schema)

    def generic_visit(self, schema: ExtendedTermSchema) -> T:
        raise NotImplementedError
