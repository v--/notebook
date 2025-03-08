import unicodedata
from collections.abc import Sequence
from typing import override

from ...parsing import Tokenizer, TokenizerContext
from .tokens import BibToken, BibTokenKind, bib_token_map


class BibTokenizer(Tokenizer[BibTokenKind]):
    @override
    def produce_token(self, context: TokenizerContext[BibTokenKind]) -> BibToken:
        if (head := self.head) and (token_type := bib_token_map.get(head)):
            self.advance()
            context.close_at_previous_token()
            return context.extract_token(token_type)

        while self.head == ' ':
            self.advance()

        if self.offset > context.offset_start:
            context.close_at_previous_token()
            return context.extract_token('SPACE')

        while (head := self.head) and head.isdigit():
            self.advance()

        if self.offset > context.offset_start:
            context.close_at_previous_token()
            return context.extract_token('NUMBER')

        while (head := self.head) and unicodedata.category(head).startswith(('L', 'Mn')):
            self.advance()

        if self.offset > context.offset_start:
            context.close_at_previous_token()
            return context.extract_token('WORD')

        if (head := self.head) and unicodedata.category(head).startswith(('S', 'P')):
            self.advance()
            context.close_at_previous_token()
            return context.extract_token('SYMBOL')

        raise self.annotate_char_error('Unexpected symbol')


def tokenize_bibtex(source: str) -> Sequence[BibToken]:
    with BibTokenizer(source) as self:
        return list(self.iter_tokens())
