from typing import TYPE_CHECKING

from .exceptions import TokenizationError
from .highlighter import ErrorHighlighter
from .tokens import Token


if TYPE_CHECKING:
    from .tokenizer import Tokenizer


class TokenizerContext[TokenKindT]:
    tokenizer: 'Tokenizer[TokenKindT]'
    offset_start: int
    offset_end: int | None

    def __init__(self, tokenizer: 'Tokenizer[TokenKindT]') -> None:
        self.tokenizer = tokenizer
        self.reset()

    def reset(self) -> None:
        self.offset_start = self.tokenizer.offset
        self.offset_end = None

    def close_at_current_token(self) -> None:
        self.offset_end = self.tokenizer.offset

    def close_at_previous_token(self) -> None:
        self.offset_end = self.tokenizer.offset - 1

    def get_offset_end_safe(self) -> int:
        if self.offset_end is None:
            return self.tokenizer.get_safe_offset()

        return self.offset_end

    def get_context_string(self) -> str:
        return self.tokenizer.source[self.offset_start: self.get_offset_end_safe() + 1]

    def extract_token(self, token_kind: TokenKindT) -> Token[TokenKindT]:
        return Token(
            kind=token_kind,
            offset=self.offset_start,
            value=self.get_context_string()
        )

    def annotate_char_error(self, message: str, offset: int | None = None) -> TokenizationError:
        err = TokenizationError(message)

        if offset is None:
            offset = self.get_offset_end_safe()

        highlighter = ErrorHighlighter(
            self.tokenizer.source,
            offset,
            offset,
            self.offset_start,
            self.get_offset_end_safe()
        )

        err.add_note(highlighter.highlight())
        return err

    def annotate_context_error(self, message: str) -> TokenizationError:
        err = TokenizationError(message)

        highlighter = ErrorHighlighter(
            self.tokenizer.source,
            self.offset_start,
            self.get_offset_end_safe()
        )

        err.add_note(highlighter.highlight())
        return err
