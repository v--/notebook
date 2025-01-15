from ..parser import Parser
from ..tokens import AbstractToken
from ..whitespace import Whitespace


class WhitespaceParserMixin[T: AbstractToken](Parser[T]):
    def skip_spaces(self) -> None:
        self.gobble_and_skip(lambda token: token == Whitespace.space)

    def skip_empty_lines(self) -> None:
        while not self.is_at_end() and self.peek() == Whitespace.line_break:
            self.advance()
            self.skip_spaces()

    def advance_and_skip_spaces(self) -> None:
        self.advance()
        self.skip_spaces()
