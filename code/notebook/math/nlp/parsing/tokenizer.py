import unicodedata
from collections.abc import Collection, Sequence
from typing import override

from ....parsing import Tokenizer, TokenizerContext
from .tokens import TextToken, TextTokenKind


ALLOWED_INTERWORD_SYMBOLS: Collection[str] = {"'", '`', '-'}


class TextTokenizer(Tokenizer[TextTokenKind]):
    def _read_word_token(self, context: TokenizerContext[TextTokenKind]) -> TextToken:
        self.advance()

        while (head := self.peek()) and (
            head in ALLOWED_INTERWORD_SYMBOLS or
            unicodedata.category(head).startswith(('L', 'Mn'))
        ):
            self.advance()

        context.close_at_previous_token()
        return context.extract_token('WORD')

    def _read_decimal_token(self, context: TokenizerContext[TextTokenKind]) -> TextToken:
        self.advance()

        while (head := self.peek()) and unicodedata.category(head).startswith('N'):
            self.advance()

        context.close_at_previous_token()
        return context.extract_token('DECIMAL')

    @override
    def read_token(self, context: TokenizerContext[TextTokenKind]) -> TextToken | None:
        # Whitespace
        while (head := self.peek()) and (head == '\t' or unicodedata.category(head).startswith('Z')):
            self.advance()

        head = self.peek()

        if head is None:
            return None

        context.reset()
        category = unicodedata.category(head)

        if category.startswith(('L', 'Mn')):
            return self._read_word_token(context)

        if category.startswith('N'):
            num_token = self._read_decimal_token(context)
            lookahead = self.peek_multiple(2)

            if len(lookahead) > 0 and lookahead[0] == '-' and unicodedata.category(lookahead[1]).startswith(('L', 'Mn')):
                self.advance()
                context.reset()
                word_token = self._read_word_token(context)
                return TextToken(
                    kind='WORD',
                    offset=num_token.offset,
                    value=num_token.value + '-' + word_token.value
                )

            return num_token

        if category.startswith(('S', 'P')):
            self.advance()
            context.close_at_previous_token()
            return context.extract_token('SYMBOL')

        if head == '\n':
            self.advance()
            context.close_at_previous_token()
            return context.extract_token('LINE_BREAK')

        raise self.annotate_char_error('Unexpected symbol')


def tokenize_text(source: str) -> Sequence[TextToken]:
    with TextTokenizer(source) as tokenizer:
        return list(tokenizer.iter_tokens())
