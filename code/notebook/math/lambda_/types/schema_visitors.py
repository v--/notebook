from .schemas import SimpleConnectiveTypeSchema, SimpleTypeSchema, TypePlaceholder
from .types import BaseType


class TypeSchemaVisitor[T]:
    def visit(self, schema: SimpleTypeSchema) -> T:
        match schema:
            case BaseType():
                return self.visit_base(schema)

            case TypePlaceholder():
                return self.visit_type_placeholder(schema)

            case SimpleConnectiveTypeSchema():
                return self.visit_connective(schema)

    def visit_base(self, schema: BaseType) -> T:
        return self.generic_visit(schema)

    def visit_type_placeholder(self, schema: TypePlaceholder) -> T:
        return self.generic_visit(schema)

    def visit_connective(self, schema: SimpleConnectiveTypeSchema) -> T:
        return self.generic_visit(schema)

    def generic_visit(self, schema: SimpleTypeSchema) -> T:
        raise NotImplementedError
