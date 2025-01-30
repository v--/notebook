from typing import NamedTuple

from ..alphabet import BinaryTypeConnective


class BaseType(NamedTuple):
    name: str

    def __str__(self) -> str:
        return str(self.name)


class SimpleConnectiveType(NamedTuple):
    conn: BinaryTypeConnective
    a: 'SimpleType'
    b: 'SimpleType'

    def __str__(self) -> str:
        return f'({self.a} {self.conn} {self.b})'


SimpleType = BaseType | SimpleConnectiveType
