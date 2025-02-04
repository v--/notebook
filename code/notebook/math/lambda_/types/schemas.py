from dataclasses import dataclass

from ....parsing.identifiers import GreekIdentifier
from ..alphabet import BinaryTypeConnective
from .types import BaseType


@dataclass(frozen=True)
class TypePlaceholder:
    identifier: GreekIdentifier

    def __str__(self) -> str:
        return str(self.identifier)


@dataclass(frozen=True)
class SimpleConnectiveTypeSchema:
    conn: BinaryTypeConnective
    a: 'SimpleTypeSchema'
    b: 'SimpleTypeSchema'

    def __str__(self) -> str:
        return f'({self.a} {self.conn} {self.b})'


SimpleTypeSchema = BaseType | TypePlaceholder | SimpleConnectiveTypeSchema
