from dataclasses import dataclass
from typing import TYPE_CHECKING, overload, override

from notebook.math.lambda_.types import (
    BaseType,
    SimpleConnectiveType,
    SimpleConnectiveTypeSchema,
    SimpleType,
    SimpleTypeSchema,
    TypePlaceholder,
    TypeSchemaVisitor,
)
from notebook.support.coderefs import collector
from notebook.support.schemas import SchemaInstantiationError


if TYPE_CHECKING:
    from .base import AtomicLambdaSchemaInstantiation


@dataclass(frozen=True)
class InstantiationVisitor(TypeSchemaVisitor[SimpleType]):
    instantiation: AtomicLambdaSchemaInstantiation

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
def instantiate_type_schema(schema: BaseType, instantiation: AtomicLambdaSchemaInstantiation) -> BaseType: ...
@overload
def instantiate_type_schema(schema: SimpleTypeSchema, instantiation: AtomicLambdaSchemaInstantiation) -> SimpleType: ...
@collector.ref('alg:simple_type_schema_instantiation')
def instantiate_type_schema(schema: SimpleTypeSchema, instantiation: AtomicLambdaSchemaInstantiation) -> SimpleType:
    return InstantiationVisitor(instantiation).visit(schema)
