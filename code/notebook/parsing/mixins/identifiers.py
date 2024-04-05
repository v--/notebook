from typing import TypeVar

from ..identifiers import AlphabeticIdentifier, Capitalization
from ..tokenizer import Tokenizer
from ..tokens import AbstractToken


T_co = TypeVar('T_co', bound=AbstractToken, covariant=True)
IdentifierT = TypeVar('IdentifierT', bound=AlphabeticIdentifier)


class IdentifierTokenizerMixin(Tokenizer[T_co]):
    def take_while_in_range(self, start: str, end: str) -> str:
        buffer: list[str] = []

        while not self.is_at_end() and start <= self.peek() <= end:
            buffer.append(self.peek())
            self.advance()

        assert len(buffer) > 0
        return ''.join(buffer)

    def _is_at_numeric_suffix(self) -> bool:
        if self.is_at_end():
            return False

        return '₀' <= self.peek() <= '₉'

    def _parse_numeric_suffix(self) -> str:
        assert self._is_at_numeric_suffix()
        digits = self.peek()
        self.advance()

        if digits == '₀' and self._is_at_numeric_suffix():
            raise self.error('Nonzero natural numbers cannot start with zero', i_first_token=self.index - 1)

        while self._is_at_numeric_suffix():
            digits += self.peek()
            self.advance()

        return digits

    def is_at_alphabetic_string(self, cls: type[AlphabeticIdentifier], capitalization: Capitalization) -> bool:
        if self.is_at_end():
            return False

        head = self.peek()

        return (
            Capitalization.small in capitalization and cls.is_small_letter(head)
        ) or (
            Capitalization.capital in capitalization and cls.is_capital_letter(head)
        )

    def parse_identifier(self, cls: type[IdentifierT], capitalization: Capitalization, *, short: bool) -> IdentifierT:
        assert self.is_at_alphabetic_string(cls, capitalization)
        symbols = self.peek()
        self.advance()

        if not short:
            while self.is_at_alphabetic_string(cls, capitalization):
                symbols += self.peek()
                self.advance()

        if self._is_at_numeric_suffix():
            symbols += self._parse_numeric_suffix()

        return cls(symbols, capitalization, short=short)
