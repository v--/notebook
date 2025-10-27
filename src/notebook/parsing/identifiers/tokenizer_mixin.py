from ...support.unicode import Capitalization, is_greek_string, is_latin_string, is_numeric_subscript_char
from ..tokenizer import Tokenizer
from ..tokenizer_context import TokenizerContext
from ..tokens import Token


class IdentifierTokenizerMixin[TokenKindT](Tokenizer[TokenKindT]):
    def read_latin_identifier(self, context: TokenizerContext[TokenKindT], token_kind: TokenKindT, capitalization: Capitalization) -> Token[TokenKindT] | None:
        if (head := self.peek()) and is_latin_string(head, capitalization):
            self.advance()

            while (head := self.peek()) and is_numeric_subscript_char(head):
                self.advance()

            context.close_at_previous_char()
            return context.extract_token(token_kind)

        return None

    def read_greek_identifier(self, context: TokenizerContext[TokenKindT], token_kind: TokenKindT, capitalization: Capitalization) -> Token[TokenKindT] | None:
        if (head := self.peek()) and is_greek_string(head, capitalization):
            self.advance()

            while (head := self.peek()) and is_numeric_subscript_char(head):
                self.advance()

            context.close_at_previous_char()
            return context.extract_token(token_kind)

        return None
