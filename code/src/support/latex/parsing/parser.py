from typing import Iterator, cast

from ...parsing.parser import Parser
from ..nodes import Command, BracelessGroup, BraceGroup, BracketGroup, LaTeXNode, Word, Whitespace, Group, Environment, SpecialNode
from .tokenizer import tokenize_latex
from .tokens import LaTeXToken, WordToken, EscapedWordToken, WhitespaceToken, SpecialToken


class LaTeXParser(Parser[LaTeXToken]):
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
        assert isinstance(self.peek(), EscapedWordToken) and cast(EscapedWordToken, self.peek()).value == 'begin'
        start_index = self.index
        self.advance()

        if self.is_at_end() or self.peek() != SpecialToken.opening_brace:
            raise self.error('No environment name specified', precede=self.index - start_index)

        self.advance()

        if self.is_at_end() or not isinstance(self.peek(), WordToken):
            raise self.error('No environment name specified', precede=self.index - start_index)

        environment = Environment(name=cast(WordToken, self.peek()).value, contents=[])
        self.advance()

        if self.is_at_end() or self.peek() != SpecialToken.closing_brace:
            raise self.error('Unclosed brace when specifying environment name', precede=self.index - start_index)

        self.advance()

        if self.is_at_end():
            raise self.error('Unmatched \\begin{%s}' % environment.name, precede=self.index - start_index)

        parsed = self.parse_iter()

        while not self.is_at_end():
            if self.peek_multiple(4) == [EscapedWordToken('end'), SpecialToken.opening_brace, WordToken(environment.name), SpecialToken.closing_brace]:
                self.advance(4)
                return environment
            else:
                environment.contents.append(next(parsed))

        raise self.error(f'Unmatched {SpecialToken.opening_brace}', precede=self.index - start_index)

    def parse_iter(self) -> Iterator[LaTeXNode]:
        while not self.is_at_end():
            head = self.peek()

            match head:
                case WhitespaceToken():
                    self.advance()
                    yield Whitespace(head.value)

                case WordToken():
                    self.advance()
                    yield Word(head.value)

                case EscapedWordToken():
                    if head.value == 'begin':
                        yield self.match_environment()
                    else:
                        self.advance()
                        yield Command(head.value)

                case SpecialToken.opening_brace:
                    yield self.match_brace(BraceGroup, SpecialToken.opening_brace, SpecialToken.closing_brace)

                case SpecialToken.opening_bracket:
                    yield self.match_brace(BracketGroup, SpecialToken.opening_bracket, SpecialToken.closing_bracket)

                case SpecialToken.closing_brace:
                    self.advance()
                    yield Word(head.value)

                case SpecialToken.closing_bracket:
                    self.advance()
                    yield Word(head.value)

                case SpecialToken.ampersand_token:
                    self.advance()
                    yield SpecialNode.ampersand

                case SpecialToken.caret_token:
                    self.advance()
                    yield SpecialNode.caret

                case SpecialToken.underscore_token:
                    self.advance()
                    yield SpecialNode.underscore

                case _:
                    raise self.error('Unexpected token')

    def parse(self):
        result = list(self.parse_iter())

        if len(result) == 1:
            return result[0]

        return BracelessGroup(contents=result)


def parse_latex(string: str) -> BracelessGroup:
    tokens = tokenize_latex(string)
    parser = LaTeXParser(tokens)
    group = parser.parse()
    parser.assert_exhausted()
    return group
