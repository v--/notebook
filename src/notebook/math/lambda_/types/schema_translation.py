from .schema_visitor import TypeSchemaVisitor
from .schemas import SimpleConnectiveTypeSchema, SimpleTypeSchema, TypePlaceholder
from .type_visitor import TypeVisitor
from .types import BaseType, SimpleConnectiveType, SimpleType, TypeVariable


class TypeToSchemaTranslator(TypeVisitor[SimpleTypeSchema]):
    def visit_base(self, type_: BaseType) -> BaseType:
        return type_

    def visit_variable(self, type_: TypeVariable) -> TypePlaceholder:
        return TypePlaceholder(type_.identifier)

    def visit_connective(self, type_: SimpleConnectiveType) -> SimpleConnectiveTypeSchema:
        return SimpleConnectiveTypeSchema(
            type_.conn,
            self.visit(type_.left),
            self.visit(type_.right)
        )


def translate_type_to_schema(type_: SimpleType) -> SimpleTypeSchema:
    return TypeToSchemaTranslator().visit(type_)


class SchemaToTypeTranslator(TypeSchemaVisitor[SimpleType]):
    def visit_base(self, schema: BaseType) -> BaseType:
        return schema

    def visit_variable(self, schema: TypeVariable) -> TypePlaceholder:
        return TypePlaceholder(schema.identifier)

    def visit_connective(self, schema: SimpleConnectiveTypeSchema) -> SimpleConnectiveType:
        return SimpleConnectiveType(
            schema.conn,
            self.visit(schema.left),
            self.visit(schema.right)
        )


def translate_schema_to_type(schema: SimpleTypeSchema) -> SimpleType:
    return SchemaToTypeTranslator().visit(schema)
