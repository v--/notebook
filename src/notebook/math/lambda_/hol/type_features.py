from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, override

from notebook.math.lambda_.terms import Constant, TypedAbstraction, TypedApplication, TypedTerm, TypedTermVisitor
from notebook.math.lambda_.terms import Variable as LambdaVariable
from notebook.math.lambda_.types import BaseType, SimpleConnectiveType, SimpleType, TypeVisitor

from . import common


if TYPE_CHECKING:
    from collections.abc import Collection, MutableSet


@dataclass
class TypeExtractionVisitor(TypedTermVisitor[None]):
    types: MutableSet[SimpleType] = field(default_factory=set)

    @override
    def visit_atomic(self, term: Constant | LambdaVariable) -> None:
        return None

    @override
    def visit_application(self, term: TypedApplication) -> None:
        self.visit(term.left)
        self.visit(term.right)

    @override
    def visit_abstraction(self, term: TypedAbstraction) -> None:
        self.types.add(term.var_type)
        self.visit(term.body)


def extract_bound_types(term: TypedTerm) -> Collection[SimpleType]:
    visitor = TypeExtractionVisitor()
    visitor.visit(term)
    return visitor.types


class TypePredicateVisitor(TypeVisitor[bool]):
    @override
    def visit_base(self, type_: BaseType) -> bool:
        return type_ == common.prop

    @override
    def visit_connective(self, type_: SimpleConnectiveType) -> bool:
        return self.visit(type_.right)


def is_predicate_type(type_: SimpleType) -> bool:
    return TypePredicateVisitor().visit(type_)


class TypeArityVisitor(TypeVisitor[int]):
    @override
    def visit_base(self, type_: BaseType) -> int:
        return 0

    @override
    def visit_connective(self, type_: SimpleConnectiveType) -> int:
        return 1 + self.visit(type_.right)


def get_type_arity(type_: SimpleType) -> int:
    return TypeArityVisitor().visit(type_)


class SubtypeVisitor(TypeVisitor[Iterable[SimpleType]]):
    @override
    def visit_base(self, type_: BaseType) -> Iterable[SimpleType]:
        yield type_

    @override
    def visit_connective(self, type_: SimpleConnectiveType) -> Iterable[SimpleType]:
        yield type_
        yield from self.visit(type_.left)
        yield from self.visit(type_.right)


def get_subtypes(type_: SimpleType) -> Iterable[SimpleType]:
    return SubtypeVisitor().visit(type_)
