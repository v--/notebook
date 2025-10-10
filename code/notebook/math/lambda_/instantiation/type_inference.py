from dataclasses import dataclass
from typing import override

from ....support.schemas import SchemaInferenceError, SchemaInstantiationError
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
class BuildInstantiationVisitor(TypeSchemaVisitor[LambdaSchemaInstantiation]):
    type: SimpleType

    @override
    def visit_base(self, schema: BaseType) -> LambdaSchemaInstantiation:
        if self.type != schema:
            raise SchemaInferenceError(f'Cannot match base type {schema} to {self.type}')

        return LambdaSchemaInstantiation()

    @override
    def visit_type_placeholder(self, schema: TypePlaceholder) -> LambdaSchemaInstantiation:
        return LambdaSchemaInstantiation(type_mapping={schema: self.type})

    @override
    def visit_connective(self, schema: SimpleConnectiveTypeSchema) -> LambdaSchemaInstantiation:
        if not isinstance(self.type, SimpleConnectiveType) or self.type.conn != schema.conn:
            raise SchemaInferenceError(f'Cannot match type schema {schema} to {self.type}')

        left = infer_instantiation_from_type(schema.left, self.type.left)
        right = infer_instantiation_from_type(schema.right, self.type.right)
        return left | right


# This is alg:simple_type_schema_inference in the monograph
def infer_instantiation_from_type(schema: SimpleTypeSchema, type_: SimpleType) -> LambdaSchemaInstantiation:
    return BuildInstantiationVisitor(type_).visit(schema)


def is_type_schema_instance(schema: SimpleTypeSchema, type_: SimpleType) -> bool:
    try:
        infer_instantiation_from_type(schema, type_)
    except SchemaInstantiationError:
        return False
    else:
        return True
