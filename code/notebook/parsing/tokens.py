from enum import Enum
from typing import Protocol, TypeVar


class AbstractToken(Protocol):
    def __str__(self) -> str:
        ...

    def __hash__(self) -> int:
        ...

    def __eq__(self, other: object) -> bool:
        ...


class TokenMixin(AbstractToken):
    value: str

    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return self.value

    def __hash__(self) -> int:
        return hash(self.value)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.value == other.value

        return False


class LiteralToken(TokenMixin):
    pass


TokenEnumT = TypeVar('TokenEnumT', bound='TokenEnum')


class TokenEnum(str, Enum):
    @classmethod
    def try_match(cls: type[TokenEnumT], value: str) -> TokenEnumT | None:
        try:
            return cls(value)
        except ValueError:
            return None

    def __str__(self) -> str:
        return self.value

    def __hash__(self) -> int:
        return hash(self.value)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.value == other.value

        return False
