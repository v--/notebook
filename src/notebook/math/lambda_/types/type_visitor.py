from ..alphabet import BinaryTypeConnective
from .types import BaseType, SimpleConnectiveType, SimpleType, TypeVariable


class TypeVisitor[T]:
    def visit(self, type_: SimpleType) -> T:
        match type_:
            case BaseType():
                return self.visit_base(type_)

            case TypeVariable():
                return self.visit_variable(type_)

            case SimpleConnectiveType():
                match type_.conn:
                    case BinaryTypeConnective.ARROW:
                        return self.visit_arrow(type_)

                    case BinaryTypeConnective.PRODUCT:
                        return self.visit_product(type_)

                    case BinaryTypeConnective.SUM:
                        return self.visit_sum(type_)

    def visit_base(self, type_: BaseType) -> T:
        return self.generic_visit(type_)

    def visit_variable(self, type_: TypeVariable) -> T:
        return self.generic_visit(type_)

    def visit_connective(self, type_: SimpleConnectiveType) -> T:
        return self.generic_visit(type_)

    def visit_arrow(self, type_: SimpleConnectiveType) -> T:
        return self.visit_connective(type_)

    def visit_product(self, type_: SimpleConnectiveType) -> T:
        return self.visit_connective(type_)

    def visit_sum(self, type_: SimpleConnectiveType) -> T:
        return self.visit_connective(type_)

    def generic_visit(self, type_: SimpleType) -> T:
        raise NotImplementedError
