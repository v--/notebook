from typing import override

from .types import BaseType, SimpleConnectiveType, SimpleType


class TypeVisitor[T]:
    def visit(self, type_: SimpleType) -> T:
        match type_:
            case BaseType():
                return self.visit_base(type_)

            case SimpleConnectiveType():
                return self.visit_connective(type_)

    def visit_base(self, type_: BaseType) -> T:
        return self.generic_visit(type_)

    def visit_connective(self, type_: SimpleConnectiveType) -> T:
        return self.generic_visit(type_)

    def generic_visit(self, type_: SimpleType) -> T:
        raise NotImplementedError


class TypeTransformationVisitor(TypeVisitor[SimpleType]):
    @override
    def visit_base(self, type_: BaseType) -> SimpleType:
        return self.generic_visit(type_)

    @override
    def visit_connective(self, type_: SimpleConnectiveType) -> SimpleType:
        return self.generic_visit(type_)
