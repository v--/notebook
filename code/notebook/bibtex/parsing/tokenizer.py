import unicodedata
from collections.abc import Sequence
from typing import override

from ...parsing.tokenizer import Tokenizer
from .tokens import BibToken, BibTokenKind, bib_token_map


class BibTokenizer(Tokenizer[BibTokenKind]):
    @override
    def get_token(self) -> BibToken | None:
        self.mark_token_start()
        head = self.peek()

        if head == ' ':
            while not self.is_at_end() and self.peek() == ' ':
                self.advance()

            return self.produce_token('SPACE', include_current=False)

        if token_type := bib_token_map.get(head):
            self.advance()
            return self.produce_token(token_type, include_current=False)

        if head.isdigit():
            while not self.is_at_end() and self.peek().isdigit():
                self.advance()

            return self.produce_token('NUMBER', include_current=False)

        category = unicodedata.category(head)

        if category.startswith(('S', 'P')):
            self.advance()
            return self.produce_token('SYMBOL', include_current=False)

        if category.startswith('L') or category == 'Mn':
            while not self.is_at_end() and unicodedata.category(self.peek()).startswith(('L', 'Mn')):
                self.advance()

            return self.produce_token('WORD', include_current=False)

        raise self.annotate_char_error(f'Unexpected symbol with Unicode category {category}')


def tokenize_bibtex(source: str) -> Sequence[BibToken]:
    with BibTokenizer(source) as tokenizer:
        return list(tokenizer.iterate_tokens())
