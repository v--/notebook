from ...parsing.parser import Parser
from ...parsing.whitespace import Whitespace
from ..nodes import (
    BraceGroup,
    BracketGroup,
    Command,
    Environment,
    Group,
    LaTeXNode,
    SpecialNode,
    Word,
)
from .tokenizer import tokenize_latex
from .tokens import EscapedWordToken, LaTeXToken, MiscToken, WordToken


class LaTeXParser(Parser[LaTeXToken]):
    def parse_brace(self, cls: type[Group], opening: LaTeXToken, closing: LaTeXToken):
        assert self.peek() == opening
        start_index = self.index
        self.advance()
        group = cls(contents=[])
        parsed_iter = self.parse()

        while not self.is_at_end() and self.peek() != closing:
            group.contents.append(next(parsed_iter))

        if self.is_at_end() or self.peek() != closing:
            raise self.error(f'Unmatched {opening}', precede=self.index - start_index)

        self.advance()
        return group

    def parse_environment(self):
        assert isinstance(head := self.peek(), EscapedWordToken) and head.value == 'begin'
        start_index = self.index
        self.advance()

        if self.is_at_end() or self.peek() != MiscToken.opening_brace:
            raise self.error('No environment name specified', precede=self.index - start_index)

        self.advance()

        if self.is_at_end() or not isinstance(head := self.peek(), WordToken):
            raise self.error('No environment name specified', precede=self.index - start_index)

        environment = Environment(name=head.value, contents=[])
        self.advance()

        if self.is_at_end() or self.peek() != MiscToken.closing_brace:
            raise self.error('Unclosed brace when specifying environment name', precede=self.index - start_index)

        self.advance()

        if self.is_at_end():
            raise self.error('Unmatched \\begin{%s}' % environment.name, precede=self.index - start_index)

        parsed_iter = self.parse()

        while not self.is_at_end():
            if self.peek_multiple(4) == [EscapedWordToken('end'), MiscToken.opening_brace, WordToken(environment.name), MiscToken.closing_brace]:
                self.advance(4)
                return environment
            else:
                environment.contents.append(next(parsed_iter))

        raise self.error(f'Unmatched {MiscToken.opening_brace}', precede=self.index - start_index)

    def parse_step(self, head: LaTeXToken) -> LaTeXNode:
        match head:
            case WordToken():
                self.advance()
                return Word(head.value)

            case EscapedWordToken():
                if head.value == 'begin':
                    return self.parse_environment()

                self.advance()
                return Command(head.value)

            case Whitespace():
                self.advance()
                return head

            case MiscToken.opening_brace:
                return self.parse_brace(BraceGroup, MiscToken.opening_brace, MiscToken.closing_brace)

            case MiscToken.opening_bracket:
                return self.parse_brace(BracketGroup, MiscToken.opening_bracket, MiscToken.closing_bracket)

            case MiscToken.closing_brace:
                self.advance()
                return Word(head.value)

            case MiscToken.closing_bracket:
                self.advance()
                return Word(head.value)

            case MiscToken.ampersand | MiscToken.underscore | MiscToken.caret:
                self.advance()
                return getattr(SpecialNode, MiscToken(head).name)

            case _:
                raise self.error('Unexpected token')

    def parse(self):
        while not self.is_at_end():
            yield self.parse_step(self.peek())


def parse_latex(string: str) -> list[LaTeXNode]:
    tokens = tokenize_latex(string)
    parser = LaTeXParser(tokens)
    result = list(parser.parse())
    parser.assert_exhausted()
    return result
