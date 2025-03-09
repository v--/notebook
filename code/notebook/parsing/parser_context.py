from .exceptions import ParsingError
from .highlighter import ErrorHighlighter
from .parser import Parser
from .tokens import Token


class ParserContext[TokenKindT]:
    parser: 'Parser[TokenKindT]'
    first_token: Token[TokenKindT]
    last_token: Token[TokenKindT] | None

    def __init__(self, parser: 'Parser[TokenKindT]') -> None:
        self.parser = parser
        self.reset()

    def reset(self) -> None:
        if head := self.parser.peek():
            self.first_token = head
        else:
            raise ParsingError('Context can be entered before end of input')

        self.last_token = None

    def close_at_current_token(self) -> None:
        try:
            self.last_token = self.parser.tokens[self.parser.token_index]
        except IndexError:
            raise ParsingError('Context can be closed before end of input') from None

    def close_at_previous_token(self) -> None:
        try:
            self.last_token = self.parser.tokens[self.parser.token_index - 1]
        except IndexError:
            raise ParsingError('Context can be closed before end of input') from None

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
