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
    left: 'SimpleTypeSchema'
    right: 'SimpleTypeSchema'

    def __str__(self) -> str:
        return f'({self.left} {self.conn} {self.right})'


SimpleTypeSchema = BaseType | TypePlaceholder | SimpleConnectiveTypeSchema
