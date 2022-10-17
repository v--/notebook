from dataclasses import dataclass
from typing import Sequence

from ..parsing import Parser
from .tokens import LaTeXToken, WordToken, EscapedWordToken, special_symbol_map, WhitespaceToken


class LaTeXTokenizer(Parser[str]):
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

    def parse(self):
        while not self.is_at_end():
            if self.peek() == '\\':
                self.advance()

                if self.peek() in (' ', '\\', '(', ')', '{', '}'):
                    yield EscapedWordToken(self.peek())
                    self.advance()
                elif 'a' <= self.peek() <= 'z' or 'A' <= self.peek() <= 'Z':
                    yield EscapedWordToken(self.capture_latin_string())
                else:
                    raise self.error('Unrecognized escape character')
            elif self.peek() in ('&', '_', '^', '{', '}', '[', ']'):
                yield special_symbol_map[self.peek()]
                self.advance()
            elif self.peek() in (' ', '\t', '\n'):
                yield self.capture_and_group_whitespace()
            else:
                yield WordToken(self.capture_word())


def tokenize_latex(string: str):
    return list(LaTeXTokenizer(string).parse())
