import unicodedata
from collections.abc import Sequence
from typing import override

from ....parsing import Tokenizer, TokenizerContext
from .tokens import SINGLETON_TOKEN_MAP, GrammarToken, GrammarTokenKind


class GrammarTokenizer(Tokenizer[GrammarTokenKind]):
    @override
    def read_token(self, context: TokenizerContext[GrammarTokenKind]) -> GrammarToken | None:
        if (head := self.peek()) and (token_type := SINGLETON_TOKEN_MAP.get(head)):
            self.advance()
            context.close_at_previous_token()
            return context.extract_token(token_type)

        while (head := self.peek()) and \
            head not in SINGLETON_TOKEN_MAP and \
            unicodedata.category(head).startswith(('L', 'Mn', 'N', 'S', 'P')):
            self.advance()

        if not context.is_empty():
            context.close_at_previous_token()
            return context.extract_token('TEXT')

        raise self.annotate_char_error('Unexpected symbol')


def tokenize_grammar(string: str) -> Sequence[GrammarToken]:
    with GrammarTokenizer(string) as tokenizer:
        return list(tokenizer.iter_tokens())
