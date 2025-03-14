from collections.abc import Sequence
from typing import override

from ....parsing import IdentifierTokenizerMixin, Tokenizer, TokenizerContext, TrieTokenizerMixin
from ....support.unicode import Capitalization
from ..signature import FormalLogicSignature, SignatureSymbol
from .tokens import SINGLETON_TOKEN_MAP, LogicToken, LogicTokenKind


class FormalLogicTokenizer(IdentifierTokenizerMixin[LogicTokenKind], TrieTokenizerMixin[LogicTokenKind, SignatureSymbol], Tokenizer[LogicTokenKind]):
    signature: FormalLogicSignature

    def __init__(self, source: str, signature: FormalLogicSignature) -> None:
        super().__init__(source)
        self.signature = signature

    @override
    def read_token(self, context: TokenizerContext[LogicTokenKind]) -> LogicToken | None:
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

        if token := self.read_latin_identifier(context, 'LATIN_IDENTIFIER', Capitalization.LOWER):
            return token

        if token := self.read_greek_identifier(context, 'GREEK_IDENTIFIER', Capitalization.LOWER):
            return token

        raise self.annotate_char_error('Unexpected symbol')


def tokenize_formal_logic_string(signature: FormalLogicSignature, source: str) -> Sequence[LogicToken]:
    with FormalLogicTokenizer(source, signature) as tokenizer:
        return list(tokenizer.iter_tokens())
