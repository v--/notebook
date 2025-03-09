from abc import ABC, abstractmethod
from collections.abc import Iterable
from types import TracebackType
from typing import Self

from .exceptions import TokenizationError
from .highlighter import ErrorHighlighter
from .tokenizer_context import TokenizerContext
from .tokens import Token


class Tokenizer[TokenKindT](ABC):
    source: str
    offset: int

    token_start_offset: int
    token_end_offset: int

    def __init__(self, source: str) -> None:
        self.source = source
        self.reset()

    def reset(self) -> None:
        self.offset = 0

    def get_safe_offset(self) -> int:
        if len(self.source) == 0:
            raise TokenizationError('Empty source')

        return min(self.offset, len(self.source) - 1)

    def peek(self) -> str | None:
        try:
            return self.source[self.offset]
        except IndexError:
            return None

    def advance(self, count: int = 1) -> None:
        self.offset += count

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
        if self.peek():
            raise self.annotate_char_error('Finished tokenizing but there is still input left')

    def iter_tokens(self) -> Iterable[Token[TokenKindT]]:
        context = TokenizerContext(self)

        while self.peek():
            context.reset()
            yield self.read_token(context)

    @abstractmethod
    def read_token(self, context: 'TokenizerContext[TokenKindT]') -> Token[TokenKindT]:
        ...
