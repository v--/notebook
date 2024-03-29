from ...parsing.tokenizer import BaseTokenizer
from .tokens import WordToken, EscapedWordToken, WhitespaceToken, SpecialToken, LaTeXToken


class LaTeXTokenizer(BaseTokenizer[LaTeXToken]):
    def capture_and_group_whitespace(self):
        length = 0
        space = self.peek()

        while not self.is_at_end() and self.peek() == space:
            length += 1
            self.advance()

        return WhitespaceToken(space * length)

    def capture_word(self):
        buffer = []

        while not self.is_at_end() and self.peek() not in (' ', '\t', '\n', '\\', '{', '}', '[', ']', '&', '_', '^'):
            buffer.append(self.peek())
            self.advance()

        if len(buffer) == 0:
            raise self.error('Expected at least one alphanumeric character')

        return ''.join(buffer)

    def capture_latin_string(self):
        buffer = []

        while not self.is_at_end() and ('a' <= self.peek() <= 'z' or 'A' <= self.peek() <= 'Z'):
            buffer.append(self.peek())
            self.advance()

        if len(buffer) == 0:
            raise self.error('Expected at least one Latin character')

        return ''.join(buffer)

    def parse_step(self, head: str):
        match head:
            case '\\':
                self.advance()

                if self.peek() in (' ', '\\', '(', ')', '{', '}'):
                    token = EscapedWordToken(self.peek())
                    self.advance()
                    return token

                if 'a' <= self.peek() <= 'z' or 'A' <= self.peek() <= 'Z':
                    return EscapedWordToken(self.capture_latin_string())

                raise self.error('Unrecognized escape character')
            case ' ' | '\t' | '\n':
                return self.capture_and_group_whitespace()
            case _ if (token := SpecialToken.try_match(head)):
                self.advance()
                return token
            case _:
                return WordToken(self.capture_word())


def tokenize_latex(string: str) -> list[LaTeXToken]:
    tokenizer = LaTeXTokenizer(string)
    tokens = list(tokenizer.parse())
    tokenizer.assert_exhausted()
    return tokens
