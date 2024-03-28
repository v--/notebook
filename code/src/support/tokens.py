from enum import Enum
from typing import Protocol


class AbstractToken(Protocol):
    def __str__(self):
        ...

    def __hash__(self):
        ...

    def __eq__(self, other: object):
        ...


class TokenMixin(AbstractToken):
    value: str

    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return self.value

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other: object):
        if isinstance(other, type(self)):
            return self.value == other.value

        return False


class TokenEnum(str, Enum):
    @classmethod
    def try_match(cls, value: str):
        try:
            return cls(value)
        except ValueError:
            return None

    def __str__(self):
        return self.value

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other: object):
        if isinstance(other, type(self)):
            return self.value == other.value

        return False
