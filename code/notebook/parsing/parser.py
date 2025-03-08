from collections.abc import Sequence
from types import TracebackType
from typing import Self

from .exceptions import ParsingError
from .highlighter import ErrorHighlighter
from .tokens import Token


class Parser[TokenKindT]:
    source: str
    tokens: Sequence[Token[TokenKindT]]
    token_index: int
    head: Token[TokenKindT] | None

    def __init__(self, source: str, tokens: Sequence[Token[TokenKindT]]) -> None:
        self.source = source
        self.tokens = tokens
        self.reset()

    def reset(self) -> None:
        self.token_index = 0

        try:
            self.head = self.tokens[self.token_index]
        except IndexError:
            self.head = None

    def peek_safe(self) -> Token[TokenKindT]:
        if len(self.tokens) == 0:
            raise ParsingError('Empty token list')

        return self.tokens[min(self.token_index, len(self.tokens) - 1)]

    def peek_multiple(self, count: int) -> Sequence[Token[TokenKindT]]:
        return self.tokens[self.token_index: self.token_index + count]

    def advance(self, count: int = 1) -> None:
        self.token_index += count

        try:
            self.head = self.tokens[self.token_index]
        except IndexError:
            self.head = None

    def annotate_token_error(self, message: str, token: Token[TokenKindT] | None = None) -> ParsingError:
        err = ParsingError(message)

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
        if self.head:
            raise self.annotate_token_error('Finished parsing but there is still input left')
