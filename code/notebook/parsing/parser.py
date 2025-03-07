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

    def __init__(self, source: str, tokens: Sequence[Token[TokenKindT]]) -> None:
        self.source = source
        self.tokens = tokens
        self.token_index = 0

    def is_at_end(self) -> bool:
        return self.token_index == len(self.tokens)

    def peek(self) -> Token[TokenKindT]:
        if len(self.tokens) == 0:
            raise ParsingError('Empty token list')

        if self.is_at_end():
            raise self.annotate_token_error('Unexpected end of input')

        return self.tokens[self.token_index]

    def peek_safe(self) -> Token[TokenKindT]:
        if len(self.tokens) == 0:
            raise ParsingError('Empty token list')

        return self.tokens[min(self.token_index, len(self.tokens) - 1)]

    def peek_multiple(self, count: int) -> Sequence[Token[TokenKindT]]:
        return self.tokens[self.token_index: self.token_index + count]

    def reset(self) -> None:
        self.token_index = 0

    def advance(self, count: int = 1) -> None:
        self.token_index += count

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
        if not self.is_at_end():
            raise self.annotate_token_error('Finished parsing but there is still input left')


class ParserTokenContext[TokenKindT]:
    parser: 'Parser[TokenKindT]'
    first_token: Token[TokenKindT]
    last_token: Token[TokenKindT] | None

    def __init__(self, parser: 'Parser[TokenKindT]') -> None:
        self.parser = parser
        self.first_token = self.parser.peek()
        self.last_token = None

    def close_at_current_token(self) -> None:
        self.last_token = self.parser.peek()

    def close_at_previous_token(self) -> None:
        self.last_token = self.parser.tokens[self.parser.token_index - 1]

    def get_last_token_safe(self) -> Token[TokenKindT]:
        return self.last_token or self.parser.peek_safe()

    def get_context_string(self) -> str:
        start = self.first_token
        end = self.get_last_token_safe()
        return self.parser.source[start.offset: end.end_offset]

    def annotate_token_error(self, message: str, token: Token[TokenKindT] | None = None) -> ParsingError:
        err = ParsingError(message)

        if token is None:
            token = self.parser.peek_safe()

        highlighter = ErrorHighlighter(
            self.parser.source,
            token.offset,
            token.end_offset - 1,
            self.first_token.offset,
            self.get_last_token_safe().end_offset - 1
        )

        err.add_note(highlighter.highlight())
        return err

    def annotate_context_error(self, message: str) -> ParsingError:
        err = ParsingError(message)

        highlighter = ErrorHighlighter(
            self.parser.source,
            self.first_token.offset,
            self.get_last_token_safe().end_offset - 1
        )

        err.add_note(highlighter.highlight())
        return err
