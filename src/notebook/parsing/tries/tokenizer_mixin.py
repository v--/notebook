from typing import TYPE_CHECKING

from notebook.parsing.tokenizer import Tokenizer
from notebook.support.collections import MissingKeyError, TrieMapping


if TYPE_CHECKING:
    from notebook.parsing.tokenizer_context import TokenizerContext
    from notebook.parsing.tokens import Token


class TrieTokenizerMixin[TokenKindT, TrieT](Tokenizer[TokenKindT]):
    def read_token_if_trie_matches(
        self,
        context: TokenizerContext[TokenKindT],
        token_kind: TokenKindT,
        trie: TrieMapping[TrieT],
    ) -> Token[TokenKindT] | None:
        increment = 0
        subtrie = trie

        while self.offset + increment < len(self.source):
            try:
                subtrie = subtrie.get_subtrie(self.source[self.offset + increment])
            except MissingKeyError:
                return None

            increment += 1

            if subtrie.matches_empty_string():
                self.advance(increment)
                context.close_at_previous_char()
                return context.extract_token(token_kind)

        return None
