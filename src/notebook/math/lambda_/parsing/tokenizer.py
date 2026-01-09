from collections.abc import Sequence
from typing import override

from ....parsing import IdentifierTokenizerMixin, Tokenizer, TokenizerContext, TrieTokenizerMixin
from ....support.unicode import Capitalization
from ..signature import LambdaSignature, SignatureSymbol
from .tokens import SINGLETON_TOKEN_MAP, LambdaToken, LambdaTokenKind


class FormalLambdaTokenizer(IdentifierTokenizerMixin[LambdaTokenKind], TrieTokenizerMixin[LambdaTokenKind, SignatureSymbol], Tokenizer[LambdaTokenKind]):
    signature: LambdaSignature

    def __init__(self, source: str, signature: LambdaSignature) -> None:
        super().__init__(source)
        self.signature = signature

    @override
    def read_token(self, context: TokenizerContext[LambdaTokenKind]) -> LambdaToken | None:
        while (head := self.peek()) and (head == ' '):
            self.advance()

        if not head:
            return None

        context.reset()

        if token_type := SINGLETON_TOKEN_MAP.get(head):
            self.advance()
            context.close_at_previous_char()
            return context.extract_token(token_type)

        if token := self.read_token_if_trie_matches(context, 'SIGNATURE_SYMBOL', self.signature.trie):
            return token

        if token := self.read_latin_identifier(context, 'SMALL_LATIN_IDENTIFIER', Capitalization.SMALL):
            return token

        if token := self.read_latin_identifier(context, 'CAPITAL_LATIN_IDENTIFIER', Capitalization.CAPITAL):
            return token

        if token := self.read_greek_identifier(context, 'SMALL_GREEK_IDENTIFIER', Capitalization.SMALL):
            return token

        raise self.annotate_char_error('Unexpected symbol')


def tokenize_lambda_string(signature: LambdaSignature, source: str) -> Sequence[LambdaToken]:
    with FormalLambdaTokenizer(source, signature) as tokenizer:
        return list(tokenizer.iter_tokens())
