from typing import NamedTuple

from ....parsing.identifiers import GreekIdentifier
from ..alphabet import BinaryTypeConnective
from .types import BaseType


class TypePlaceholder(NamedTuple):
    identifier: GreekIdentifier

    def __str__(self) -> str:
        return str(self.identifier)


class SimpleConnectiveTypeSchema(NamedTuple):
    conn: BinaryTypeConnective
    a: 'SimpleTypeSchema'
    b: 'SimpleTypeSchema'

    def __str__(self) -> str:
        return f'({self.a} {self.conn} {self.b})'


SimpleTypeSchema = BaseType | TypePlaceholder | SimpleConnectiveTypeSchema
