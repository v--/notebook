from typing import override

from .types import BaseType, SimpleConnectiveType, SimpleType


class TypeVisitor[T]:
    def visit(self, schema: SimpleType) -> T:
        match schema:
            case BaseType():
                return self.visit_base(schema)

            case SimpleConnectiveType():
                return self.visit_connective(schema)

    def visit_base(self, schema: BaseType) -> T:
        return self.generic_visit(schema)

    def visit_connective(self, schema: SimpleConnectiveType) -> T:
        return self.generic_visit(schema)

    def generic_visit(self, schema: SimpleType) -> T:
        raise NotImplementedError


class TypeTransformationVisitor(TypeVisitor[SimpleType]):
    @override
    def visit_base(self, schema: BaseType) -> SimpleType:
        return self.generic_visit(schema)

    @override
    def visit_connective(self, schema: SimpleConnectiveType) -> SimpleType:
        return self.generic_visit(schema)
