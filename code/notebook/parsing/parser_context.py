from collections.abc import Sequence

from .exceptions import ParsingError
from .highlighter import ErrorHighlighter
from .parser import Parser
from .tokens import Token


class ParserContext[TokenKindT]:
    parser: 'Parser[TokenKindT]'
    index_start: int
    index_end: int | None

    def __init__(self, parser: 'Parser[TokenKindT]') -> None:
        self.parser = parser
        self.reset()

    def reset(self) -> None:
        self.index_start = self.parser.token_index
        self.index_end = None

        try:
            self.parser.tokens[self.index_start]
        except IndexError:
            raise ParsingError('Context can be entered before end of input') from None

    def is_closed(self) -> bool:
        return self.index_end is not None

    def close_at_current_token(self) -> None:
        self.index_end = self.parser.token_index

        try:
            self.parser.tokens[self.index_end]
        except IndexError:
            raise ParsingError('Context can be closed before end of input') from None

    def close_at_previous_token(self) -> None:
        self.index_end = self.parser.token_index - 1

        try:
            self.parser.tokens[self.index_end]
        except IndexError:
            raise ParsingError('Context can be closed before end of input') from None

    def get_index_end_safe(self) -> int:
        if self.index_end is None:
            return self.parser.get_safe_token_index()

        return self.index_end

    def is_empty(self) -> bool:
        return self.index_start == self.get_index_end_safe()

    def get_first_token(self) -> Token[TokenKindT]:
        return self.parser.tokens[self.index_start]

    def get_last_token_safe(self) -> Token[TokenKindT]:
        return self.parser.tokens[self.get_index_end_safe()]

    def get_context_tokens(self) -> Sequence[Token[TokenKindT]]:
        start = self.index_start
        end = self.get_index_end_safe()
        return self.parser.tokens[start: end + 1]

    def get_context_string(self) -> str:
        start = self.get_first_token()
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
            self.get_first_token().offset,
            self.get_last_token_safe().end_offset - 1
        )

        err.add_note(highlighter.highlight())
        return err

    def annotate_context_error(self, message: str) -> ParsingError:
        err = ParsingError(message)

        highlighter = ErrorHighlighter(
            self.parser.source,
            self.get_first_token().offset,
            self.get_last_token_safe().end_offset - 1
        )

        err.add_note(highlighter.highlight())
        return err
