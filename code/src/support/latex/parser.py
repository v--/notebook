from __future__ import annotations

from typing import Iterator, Sequence

from ..parsing import Parser
from .tokenizer import tokenize_latex
from .tokens import LaTeXToken, WordToken, EscapedWordToken, opening_brace, closing_brace, opening_bracket, closing_bracket, WhitespaceToken, underscore_token, caret_token, ampersand_token
from .nodes import Command, BracelessGroup, BraceGroup, BracketGroup, LaTeXNode, Word, Whitespace, Group, Environment, underscore, caret, ampersand


class LaTeXParser(Parser[Sequence[LaTeXToken]]):
    def match_brace(self, cls: type[Group], opening: LaTeXToken, closing: LaTeXToken):
        assert self.peek() == opening
        start_index = self.index
        self.advance()
        group = cls(contents=[])
        parsed = self.parse_iter()

        while not self.is_at_end() and self.peek() != closing:
            group.contents.append(next(parsed))

        if self.is_at_end() or self.peek() != closing:
            raise self.error(f'Unmatched {opening}', precede=self.index - start_index)

        self.advance()
        return group

    def match_environment(self):
        assert isinstance(self.peek(), EscapedWordToken) and self.peek().value == 'begin'
        start_index = self.index
        self.advance()

        if self.is_at_end() or self.peek() != opening_brace:
            raise self.error(f'No environment name specified', precede=self.index - start_index)

        self.advance()
        if self.is_at_end() or not isinstance(self.peek(), WordToken):
            raise self.error(f'No environment name specified', precede=self.index - start_index)

        environment = Environment(name=self.peek().value, contents=[])
        self.advance()

        if self.is_at_end() or self.peek() != closing_brace:
            raise self.error(f'Unclosed brace when specifying environment name', precede=self.index - start_index)

        self.advance()

        if self.is_at_end():
            raise self.error('Unmatched \\begin{%s}' % environment.name, precede=self.index - start_index)

        parsed = self.parse_iter()

        while not self.is_at_end():
            if self.seq[self.index:self.index + 4] == [EscapedWordToken('end'), opening_brace, WordToken(environment.name), closing_brace]:
                self.advance(4)
                return environment
            else:
                environment.contents.append(next(parsed))

        raise self.error(f'Unmatched {opening_brace}', precede=self.index - start_index)

    def parse_iter(self) -> Iterator[LaTeXNode]:
        while not self.is_at_end():
            head = self.peek()

            if isinstance(head, WhitespaceToken):
                self.advance()
                yield Whitespace(head.value)

            elif isinstance(head, WordToken):
                self.advance()
                yield Word(head.value)

            elif isinstance(head, EscapedWordToken):
                if head.value == 'begin':
                    yield self.match_environment()
                else:
                    self.advance()
                    yield Command(head.value)

            elif head == opening_brace:
                yield self.match_brace(BraceGroup, opening_brace, closing_brace)

            elif head == opening_bracket:
                yield self.match_brace(BracketGroup, opening_bracket, closing_bracket)

            elif head == closing_brace:
                self.advance()
                yield Word(head.value)

            elif head == closing_bracket:
                self.advance()
                yield Word(head.value)

            elif head == ampersand_token:
                self.advance()
                yield ampersand

            elif head == caret_token:
                self.advance()
                yield caret

            elif head == underscore_token:
                self.advance()
                yield underscore

            else:
                raise self.error('Unexpected token')

    def parse(self):
        result = list(self.parse_iter())

        if len(result) == 1:
            return result[0]

        return BracelessGroup(contents=result)


def parse_latex(string: str):
    return LaTeXParser(tokenize_latex(string)).parse()
