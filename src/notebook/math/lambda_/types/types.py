from dataclasses import dataclass

from ....parsing.identifiers import GreekIdentifier
from ..alphabet import BinaryTypeConnective
from ..signature import BaseTypeSymbol


@dataclass(frozen=True)
class BaseType:
    value: BaseTypeSymbol

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"parse_type('{self}')"


@dataclass(frozen=True)
class TypeVariable:
    identifier: GreekIdentifier

    def __str__(self) -> str:
        return str(self.identifier)

    def __repr__(self) -> str:
        return f"parse_type('{self}')"


@dataclass(frozen=True)
class SimpleConnectiveType:
    conn: BinaryTypeConnective
    left: SimpleType
    right: SimpleType

    def __str__(self) -> str:
        return f'({self.left} {self.conn} {self.right})'

    def __repr__(self) -> str:
        return f"parse_type('{self}')"


SimpleType = BaseType | TypeVariable | SimpleConnectiveType
