from abc import ABC, abstractmethod
from collections.abc import Iterable
from types import TracebackType
from typing import Self

from .exceptions import TokenizationError
from .highlighter import ErrorHighlighter
from .tokens import Token


class Tokenizer[TokenKindT](ABC):
    source: str
    offset: int
    token_start_offset: int

    def __init__(self, source: str) -> None:
        self.source = source
        self.offset = 0
        self.reset()
        self.mark_token_start()

    def is_at_end(self) -> bool:
        return self.offset == len(self.source)

    def get_safe_offset(self) -> int:
        if len(self.source) == 0:
            raise TokenizationError('Empty source')

        return min(self.offset, len(self.source) - 1)

    def peek(self) -> str:
        if len(self.source) == 0:
            raise TokenizationError('Empty source')

        if self.is_at_end():
            self.annotate_char_error('Unexpected end of input')

        return self.source[self.offset]

    def reset(self) -> None:
        self.offset = 0

    def advance(self, count: int = 1) -> None:
        self.offset += count

    def mark_token_start(self) -> None:
        self.token_start_offset = self.offset

    def annotate_char_error(self, message: str, offset: int | None = None) -> TokenizationError:
        err = TokenizationError(message)

        if offset is None:
            offset = self.get_safe_offset()

        highlighter = ErrorHighlighter(self.source, offset, offset)
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
            raise self.annotate_char_error('Finished tokenizing but there is still input left')

    def produce_token(self, token_kind: TokenKindT, *, include_current: bool) -> Token[TokenKindT]:
        return Token(
            kind=token_kind,
            offset=self.token_start_offset,
            # The character at the offset should already belong to the next token.
            # Fortunately, Python indexing cuts off the end.
            value=self.source[self.token_start_offset: self.offset + int(include_current)]
        )

    def iterate_tokens(self) -> Iterable[Token[TokenKindT]]:
        while not self.is_at_end():
            if token := self.get_token():
                yield token

    @abstractmethod
    def get_token(self) -> Token[TokenKindT] | None:
        ...
