from abc import ABC, abstractmethod
from typing import Generic, Iterable, TypeVar

from .identifiers import AlphabeticIdentifier, Capitalization
from .parser import Parser
from .tokens import AbstractToken


T_co = TypeVar('T_co', bound=AbstractToken, covariant=True)


class Tokenizer(Generic[T_co], Parser[str], ABC):
    def parse(self) -> Iterable[T_co]:
        while not self.is_at_end():
            yield self.parse_step(self.peek())

    @abstractmethod
    def parse_step(self, head: str) -> T_co:
        ...
