from ...parsing.tokenizer import Tokenizer
from .tokens import WordToken, EscapedWordToken, MiscToken, LaTeXToken


class LaTeXTokenizer(Tokenizer[LaTeXToken]):
    def accept_word(self):
        buffer = []

        while not self.is_at_end() and self.peek() not in (' ', '\t', '\n', '\\', '{', '}', '[', ']', '&', '_', '^'):
            buffer.append(self.peek())
            self.advance()

        if len(buffer) == 0:
            raise self.error('Expected at least one alphanumeric character')

        return ''.join(buffer)

    def accept_latin_string(self):
        buffer = []

        while not self.is_at_end() and ('a' <= self.peek() <= 'z' or 'A' <= self.peek() <= 'Z'):
            buffer.append(self.peek())
            self.advance()

        if len(buffer) == 0:
            raise self.error('Expected at least one Latin character')

        return ''.join(buffer)

    def parse_step(self, head: str):
        if (token := MiscToken.try_match(head)):
            self.advance()
            return token

        if head == '\\':
            self.advance()

            if self.peek() in (' ', '\\', '(', ')', '{', '}'):
                token = EscapedWordToken(self.peek())
                self.advance()
                return token

            if 'a' <= self.peek() <= 'z' or 'A' <= self.peek() <= 'Z':
                return EscapedWordToken(self.accept_latin_string())

            raise self.error('Unrecognized escape character')

        return WordToken(self.accept_word())


def tokenize_latex(string: str) -> list[LaTeXToken]:
    tokenizer = LaTeXTokenizer(string)
    tokens = list(tokenizer.parse())
    tokenizer.assert_exhausted()
    return tokens
