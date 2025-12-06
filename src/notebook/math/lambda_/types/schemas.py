from dataclasses import dataclass

from ....parsing.identifiers import GreekIdentifier
from ..alphabet import BinaryTypeConnective
from .types import BaseType


@dataclass(frozen=True)
class TypePlaceholder:
    identifier: GreekIdentifier

    def __str__(self) -> str:
        return str(self.identifier)

    def __repr__(self) -> str:
        return f"parse_type_schema('{self}')"


@dataclass(frozen=True)
class SimpleConnectiveTypeSchema:
    conn: BinaryTypeConnective
    left: SimpleTypeSchema
    right: SimpleTypeSchema

    def __str__(self) -> str:
        return f'({self.left} {self.conn} {self.right})'

    def __repr__(self) -> str:
        return f"parse_type_schema('{self}')"


SimpleTypeSchema = BaseType | TypePlaceholder | SimpleConnectiveTypeSchema
