from typing import override

from ...parsing import ErrorHighlighter, Parser, ParserContext, ParsingError
from ..string import CompositeStringBuilder
from .tokens import BibToken, BibTokenKind


class BibEntryContext(ParserContext[BibTokenKind]):
    pass


class BibValueContext(ParserContext[BibTokenKind]):
    entry_context: BibEntryContext | None

    def __init__(self, parser: Parser[BibTokenKind], entry_context: BibEntryContext | None) -> None:
        super().__init__(parser)
        self.entry_context = entry_context
        self.string_builder = CompositeStringBuilder()

    @override
    def annotate_context_error(self, message: str) -> ParsingError:
        err = ParsingError(message)

        first_token = self.get_first_token()
        last_token = self.get_last_token_safe()

        if self.entry_context:
            first_shown_token = self.entry_context.get_first_token()
            last_shown_token = self.entry_context.get_last_token_safe()
        else:
            first_shown_token = first_token
            last_shown_token = last_token

        highlighter = ErrorHighlighter(
            self.parser.source,
            first_token.offset,
            last_token.end_offset - 1,
            first_shown_token.offset,
            last_shown_token.end_offset - 1
        )

        err.add_note(highlighter.highlight())
        return err

    @override
    def annotate_token_error(self, message: str, token: BibToken | None = None) -> ParsingError:
        if self.entry_context:
            return self.entry_context.annotate_token_error(message, token)

        return super().annotate_token_error(message, token)
