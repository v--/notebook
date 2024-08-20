from abc import ABC, abstractmethod
from typing import Iterable

from .parser import Parser
from .tokens import AbstractToken


class Tokenizer[T_co: AbstractToken](Parser[str], ABC):
    def parse(self) -> Iterable[T_co]:
        while not self.is_at_end():
            yield self.parse_step(self.peek())

    @abstractmethod
    def parse_step(self, head: str) -> T_co:
        ...
