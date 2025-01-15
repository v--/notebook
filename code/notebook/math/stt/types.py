from typing import NamedTuple

from ...parsing.identifiers import GreekIdentifier
from .alphabet import SimpleTypeConnective


class BaseType(NamedTuple):
    name: str

    def __str__(self) -> str:
        return str(self.name)


class ArrowType(NamedTuple):
    a: 'SimpleType'
    b: 'SimpleType'

    def __str__(self) -> str:
        return f'({self.a} {SimpleTypeConnective.arrow} {self.b})'


SimpleType = BaseType | ArrowType


class SimpleTypePlaceholder(NamedTuple):
    identifier: GreekIdentifier

    def __str__(self) -> str:
        return str(self.identifier)


class ArrowTypeSchema(NamedTuple):
    a: 'SimpleTypeSchema'
    b: 'SimpleTypeSchema'

    def __str__(self) -> str:
        return f'({self.a} {SimpleTypeConnective.arrow} {self.b})'


SimpleTypeSchema = BaseType | SimpleTypePlaceholder | ArrowTypeSchema
