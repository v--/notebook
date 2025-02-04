from dataclasses import dataclass

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
