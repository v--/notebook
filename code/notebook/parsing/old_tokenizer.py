from abc import ABC, abstractmethod
from collections.abc import Iterable

from .old_parser import Parser
from .old_tokens import AbstractToken


class Tokenizer[T: AbstractToken](Parser[str], ABC):
    def parse(self) -> Iterable[T]:
        while not self.is_at_end():
            yield self.parse_step(self.peek())

    @abstractmethod
    def parse_step(self, head: str) -> T:
        ...
