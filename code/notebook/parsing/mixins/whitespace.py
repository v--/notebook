from typing import TypeVar

from ..tokenizer import Parser
from ..tokens import AbstractToken
from ..whitespace import Whitespace


T_co = TypeVar('T_co', bound=AbstractToken, covariant=True)


class WhitespaceParserMixin(Parser[T_co]):
    def skip_spaces(self) -> None:
        while not self.is_at_end() and self.peek() == Whitespace.space:
            self.advance()

    def skip_empty_lines(self) -> None:
        while not self.is_at_end() and self.peek() == Whitespace.line_break:
            self.advance()
            self.skip_spaces()

    def advance_and_skip_spaces(self) -> None:
        self.advance()
        self.skip_spaces()
