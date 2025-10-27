from .types import BaseType, SimpleConnectiveType, SimpleType, TypeVariable


class TypeVisitor[T]:
    def visit(self, type_: SimpleType) -> T:
        match type_:
            case BaseType():
                return self.visit_base(type_)

            case TypeVariable():
                return self.visit_variable(type_)

            case SimpleConnectiveType():
                return self.visit_connective(type_)

    def visit_base(self, type_: BaseType) -> T:
        return self.generic_visit(type_)

    def visit_variable(self, type_: TypeVariable) -> T:
        return self.generic_visit(type_)

    def visit_connective(self, type_: SimpleConnectiveType) -> T:
        return self.generic_visit(type_)

    def generic_visit(self, type_: SimpleType) -> T:
        raise NotImplementedError
