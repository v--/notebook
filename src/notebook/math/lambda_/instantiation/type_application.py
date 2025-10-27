from dataclasses import dataclass
from typing import overload, override

from ....support.schemas import SchemaInstantiationError
from ..types import (
    BaseType,
    SimpleConnectiveType,
    SimpleConnectiveTypeSchema,
    SimpleType,
    SimpleTypeSchema,
    TypePlaceholder,
    TypeSchemaVisitor,
)
from .base import LambdaSchemaInstantiation


@dataclass(frozen=True)
class InstantiationVisitor(TypeSchemaVisitor[SimpleType]):
    instantiation: LambdaSchemaInstantiation

    @override
    def visit_base(self, schema: BaseType) -> BaseType:
        return schema

    @override
    def visit_type_placeholder(self, schema: TypePlaceholder) -> SimpleType:
        if schema not in self.instantiation.type_mapping:
            raise SchemaInstantiationError(f'No specification of how to instantiate the type placeholder {schema}')

        return self.instantiation.type_mapping[schema]

    @override
    def visit_connective(self, schema: SimpleConnectiveTypeSchema) -> SimpleConnectiveType:
        return SimpleConnectiveType(schema.conn, self.visit(schema.left), self.visit(schema.right))


@overload
def instantiate_type_schema(schema: BaseType, instantiation: LambdaSchemaInstantiation) -> BaseType: ...
@overload
def instantiate_type_schema(schema: SimpleTypeSchema, instantiation: LambdaSchemaInstantiation) -> SimpleType: ...
def instantiate_type_schema(schema: SimpleTypeSchema, instantiation: LambdaSchemaInstantiation) -> SimpleType:
    return InstantiationVisitor(instantiation).visit(schema)
