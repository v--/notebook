from ...support.unicode import Capitalization, atoi_subscripts, is_greek_string, is_latin_string, is_numeric_subscript
from ..identifiers import GreekIdentifier, LatinIdentifier
from ..old_tokenizer import Tokenizer
from ..old_tokens import AbstractToken


class IdentifierTokenizerMixin[T: AbstractToken](Tokenizer[T]):
    def _is_at_numeric_suffix(self) -> bool:
        if self.is_at_end():
            return False

        return is_numeric_subscript(self.peek())

    def _parse_numeric_suffix(self) -> int:
        assert self._is_at_numeric_suffix()
        digits = self.peek()
        self.advance()

        if digits == '₀' and self._is_at_numeric_suffix():
            raise self.error('Nonzero natural numbers cannot start with zero', i_first_token=self.index - 1)

        while self._is_at_numeric_suffix():
            digits += self.peek()
            self.advance()

        return atoi_subscripts(digits)

    def parse_latin_identifier(self, capitalization: Capitalization = Capitalization.lower) -> LatinIdentifier:
        assert is_latin_string(self.peek(), capitalization)
        letter = self.peek()
        self.advance()

        return LatinIdentifier(
            letter,
            self._parse_numeric_suffix() if self._is_at_numeric_suffix() else None
        )

    def parse_greek_identifier(self, capitalization: Capitalization = Capitalization.lower) -> GreekIdentifier:
        assert is_greek_string(self.peek(), capitalization)
        letter = self.peek()
        self.advance()

        return GreekIdentifier(
            letter,
            self._parse_numeric_suffix() if self._is_at_numeric_suffix() else None
        )
