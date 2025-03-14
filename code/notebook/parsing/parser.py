from collections.abc import Sequence
from types import TracebackType
from typing import Self

from .exceptions import ParserError
from .highlighter import ErrorHighlighter
from .tokens import Token


class Parser[TokenT: Token]:
    source: str
    tokens: Sequence[TokenT]
    token_index: int

    def __init__(self, source: str, tokens: Sequence[TokenT]) -> None:
        self.source = source
        self.tokens = tokens
        self.reset()

    def reset(self) -> None:
        self.token_index = 0

    def peek(self) -> TokenT | None:
        try:
            return self.tokens[self.token_index]
        except IndexError:
            return None

    def get_safe_token_index(self) -> int:
        if len(self.tokens) == 0:
            raise ParserError('Empty token list')

        return min(self.token_index, len(self.tokens) - 1)

    def annotate_unexpected_end_of_input(self) -> ParserError:
        if self.source == '':
            return ParserError('Empty input')

        return self.annotate_token_error('Unexpected end of input')

    def peek_unsafe(self) -> TokenT:
        try:
            return self.tokens[self.token_index]
        except IndexError:
            raise self.annotate_unexpected_end_of_input() from None

    def peek_safe(self) -> TokenT:
        return self.tokens[self.get_safe_token_index()]

    def peek_multiple(self, count: int) -> Sequence[TokenT]:
        return self.tokens[self.token_index: self.token_index + count]

    def advance(self, count: int = 1) -> None:
        self.token_index += count

    def advance_and_peek(self, count: int = 1) -> TokenT | None:
        self.advance(count)
        return self.peek()

    def annotate_token_error(self, message: str, token: TokenT | None = None) -> ParserError:
        err = ParserError(message)

        if token is None:
            token = self.peek_safe()

        highlighter = ErrorHighlighter(
            self.source,
            token.offset,
            token.end_offset - 1,
        )

        err.add_note(highlighter.highlight())
        return err

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None
     ) -> None:
        if exc_type is None:
            self.assert_exhausted()

    def assert_exhausted(self) -> None:
        if self.peek():
            raise self.annotate_token_error('Finished parsing but there is still input left')
