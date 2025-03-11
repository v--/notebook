import unicodedata
from collections.abc import Sequence
from typing import override

from ...parsing import Tokenizer, TokenizerContext
from .tokens import SINGLETON_TOKEN_MAP, LaTeXToken, LaTeXTokenKind


class LaTeXTokenizer(Tokenizer[LaTeXTokenKind]):
    @override
    def read_token(self, context: TokenizerContext[LaTeXTokenKind]) -> LaTeXToken:
        if (head := self.peek()) and (token_type := SINGLETON_TOKEN_MAP.get(head)):
            self.advance()
            context.close_at_previous_token()
            return context.extract_token(token_type)

        while (head := self.peek()) and (head == ' ' or head == '\t'):
            self.advance()

        if not context.is_empty():
            context.close_at_previous_token()
            return context.extract_token('WHITESPACE')

        while (head := self.peek()) and \
            head not in SINGLETON_TOKEN_MAP and \
            unicodedata.category(head).startswith(('L', 'Mn', 'N', 'S', 'P')):
            self.advance()

        if not context.is_empty():
            context.close_at_previous_token()
            return context.extract_token('TEXT')

        raise self.annotate_char_error('Unexpected symbol')


def tokenize_latex(source: str) -> Sequence[LaTeXToken]:
    with LaTeXTokenizer(source) as tokenizer:
        return list(tokenizer.iter_tokens())
