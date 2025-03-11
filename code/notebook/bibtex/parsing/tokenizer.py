import unicodedata
from collections.abc import Sequence
from typing import override

from ...parsing import Tokenizer, TokenizerContext
from .tokens import SINGLETON_TOKEN_MAP, BibToken, BibTokenKind


class BibTokenizer(Tokenizer[BibTokenKind]):
    @override
    def read_token(self, context: TokenizerContext[BibTokenKind]) -> BibToken:
        if (head := self.peek()) and (token_type := SINGLETON_TOKEN_MAP.get(head)):
            self.advance()
            context.close_at_previous_token()
            return context.extract_token(token_type)

        while (head := self.peek()) and head.isdigit():
            self.advance()

        if not context.is_empty():
            context.close_at_previous_token()
            return context.extract_token('DECIMAL')

        while (head := self.peek()) and unicodedata.category(head).startswith(('L', 'Mn')):
            self.advance()

        if not context.is_empty():
            context.close_at_previous_token()
            return context.extract_token('WORD')

        if (head := self.peek()) and unicodedata.category(head).startswith(('S', 'P')):
            self.advance()
            context.close_at_previous_token()
            return context.extract_token('SYMBOL')

        raise self.annotate_char_error('Unexpected symbol')


def tokenize_bibtex(source: str) -> Sequence[BibToken]:
    with BibTokenizer(source) as tokenizer:
        return list(tokenizer.iter_tokens())
