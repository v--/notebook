from dataclasses import dataclass
from typing import TypeGuard

from ..alphabet import BinaryTypeConnective


@dataclass(frozen=True)
class BaseType:
    name: str

    def __str__(self) -> str:
        return str(self.name)


@dataclass(frozen=True)
class SimpleConnectiveType:
    conn: BinaryTypeConnective
    a: 'SimpleType'
    b: 'SimpleType'

    def __str__(self) -> str:
        return f'({self.a} {self.conn} {self.b})'


SimpleType = BaseType | SimpleConnectiveType


def is_arrow_type(type_: SimpleType) -> TypeGuard[SimpleConnectiveType]:
    return isinstance(type_, SimpleConnectiveType) and type_.conn == BinaryTypeConnective.arrow


def is_product_type(type_: SimpleType) -> TypeGuard[SimpleConnectiveType]:
    return isinstance(type_, SimpleConnectiveType) and type_.conn == BinaryTypeConnective.arrow


def is_sum_type(type_: SimpleType) -> TypeGuard[SimpleConnectiveType]:
    return isinstance(type_, SimpleConnectiveType) and type_.conn == BinaryTypeConnective.arrow
