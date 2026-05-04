from notebook.parsing.identifiers import GreekIdentifier, LatinIdentifier
from notebook.parsing.parser import Parser
from notebook.parsing.tokens import Token
from notebook.support.unicode import atoi_subscripts


class IdentifierParserMixin[TokenKindT, TokenT: Token](Parser[TokenT]):
    def _parse_decimal_subscript(self, string: str) -> int:
        if len(string) > 1 and string.startswith('₀'):
            raise self.annotate_token_error('Nonzero subscripts cannot start with zero')

        return atoi_subscripts(string)

    def parse_latin_identifier(self, token_kind: TokenKindT) -> LatinIdentifier:
        head = self.peek()

        if not head:
            raise self.annotate_unexpected_end_of_input()

        if head.kind != token_kind:
            raise self.annotate_token_error(f'Unexpected token kind {head.kind}')

        letter = head.value[0]
        subscript = head.value[1:]
        self.advance()

        if len(subscript) > 0:
            index = self._parse_decimal_subscript(subscript)
            return LatinIdentifier(letter, index)

        return LatinIdentifier(letter)

    def parse_greek_identifier(self, token_kind: TokenKindT) -> GreekIdentifier:
        head = self.peek()

        if not head:
            raise self.annotate_unexpected_end_of_input()

        if head.kind != token_kind:
            raise self.annotate_token_error(f'Unexpected token kind {head.kind}')

        letter = head.value[0]
        subscript = head.value[1:]
        self.advance()

        if len(subscript) > 0:
            index = self._parse_decimal_subscript(subscript)
            return GreekIdentifier(letter, index)

        return GreekIdentifier(letter)
