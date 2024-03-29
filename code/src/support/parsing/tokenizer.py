from abc import ABC, abstractmethod
from typing import Generic, Iterable, TypeVar

from .parser import Parser
from .tokens import AbstractToken
from .identifiers import Capitalization, AlphabeticIdentifier


T_co = TypeVar('T_co', bound=AbstractToken, covariant=True)
TIdentifier = TypeVar('TIdentifier', bound=AlphabeticIdentifier)


class BaseTokenizer(Generic[T_co], Parser[str], ABC):
    def take_while_in_range(self, start: str, end: str):
        buffer: list[str] = []

        while not self.is_at_end() and start <= self.peek() <= end:
            buffer.append(self.peek())
            self.advance()

        assert len(buffer) > 0
        return ''.join(buffer)

    def parse(self) -> Iterable[T_co]:
        while not self.is_at_end():
            yield self.parse_step(self.peek())

    def _accept_numeric_suffix(self):
        if self.is_at_end():
            return False

        return '₀' <= self.peek() <= '₉'

    def _parse_numeric_suffix(self):
        assert self._accept_numeric_suffix()
        digits = self.peek()
        self.advance()

        if digits == '₀' and self._accept_numeric_suffix():
            raise self.error('Nonzero natural numbers cannot start with zero')

        while self._accept_numeric_suffix():
            digits += self.peek()
            self.advance()

        return digits

    def accept_alphabetic_string(self, cls: type[AlphabeticIdentifier], capitalization: Capitalization):
        if self.is_at_end():
            return False

        head = self.peek()

        return (
            Capitalization.small in capitalization and cls.is_small_letter(head)
        ) or (
            Capitalization.capital in capitalization and cls.is_capital_letter(head)
        )

    def parse_identifier(self, cls: type[TIdentifier], capitalization: Capitalization, short: bool) -> TIdentifier:
        assert self.accept_alphabetic_string(cls, capitalization)
        symbols = self.peek()
        self.advance()

        if not short:
            while self.accept_alphabetic_string(cls, capitalization):
                symbols += self.peek()
                self.advance()

        if self._accept_numeric_suffix():
            symbols += self._parse_numeric_suffix()

        return cls(symbols, capitalization, short)

    @abstractmethod
    def parse_step(self, head: str) -> T_co:
        ...
