from .schemas import FunctionApplicationSchema, TermPlaceholder, TermSchema, VariablePlaceholder


class TermSchemaVisitor[T]:
    def visit(self, schema: TermSchema) -> T:
        match schema:
            case VariablePlaceholder():
                return self.visit_variable_placeholder(schema)

            case TermPlaceholder():
                return self.visit_term_placeholder(schema)

            case FunctionApplicationSchema():
                return self.visit_function(schema)

    def visit_variable_placeholder(self, schema: VariablePlaceholder) -> T:
        return self.generic_visit(schema)

    def visit_term_placeholder(self, schema: TermPlaceholder) -> T:
        return self.generic_visit(schema)

    def visit_function(self, schema: FunctionApplicationSchema) -> T:
        return self.generic_visit(schema)

    def generic_visit(self, schema: TermSchema) -> T:
        raise NotImplementedError
