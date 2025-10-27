from dataclasses import dataclass
from typing import TypeGuard

from ....parsing.identifiers import GreekIdentifier
from ..alphabet import BinaryTypeConnective


@dataclass(frozen=True)
class BaseType:
    name: str

    def __str__(self) -> str:
        return str(self.name)


@dataclass(frozen=True)
class TypeVariable:
    identifier: GreekIdentifier

    def __str__(self) -> str:
        return str(self.identifier)


@dataclass(frozen=True)
class SimpleConnectiveType:
    conn: BinaryTypeConnective
    left: SimpleType
    right: SimpleType

    def __str__(self) -> str:
        return f'({self.left} {self.conn} {self.right})'


SimpleType = BaseType | TypeVariable | SimpleConnectiveType


def is_arrow_type(type_: SimpleType) -> TypeGuard[SimpleConnectiveType]:
    return isinstance(type_, SimpleConnectiveType) and type_.conn == BinaryTypeConnective.ARROW


def is_product_type(type_: SimpleType) -> TypeGuard[SimpleConnectiveType]:
    return isinstance(type_, SimpleConnectiveType) and type_.conn == BinaryTypeConnective.PROD


def is_sum_type(type_: SimpleType) -> TypeGuard[SimpleConnectiveType]:
    return isinstance(type_, SimpleConnectiveType) and type_.conn == BinaryTypeConnective.SUM
