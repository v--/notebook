from typing import Iterable

from ..support.parsing.parser import Parser, ParserError

from .tokens import LambdaToken, LatinLetter, NaturalNumber, MiscToken

from .terms import Variable, Application, Abstraction


class IncompleteMatchError(ParserError):
    pass


class LambdaTokenizer(Parser[str]):
    def parse_natural_number(self):
        if self.peek() == '0':
            raise self.error('Natural numbers cannot start with zero')

        buffer: list[str] = []

        while not self.is_at_end() and self.peek().isdigit():
            buffer.append(self.peek())
            self.advance()

        assert len(buffer) > 0
        return NaturalNumber(''.join(buffer))

    def parse(self) -> Iterable[LambdaToken]:
        while not self.is_at_end():
            yield self.parse_step(self.peek())

    def parse_step(self, head: str):
        sym = MiscToken.try_match(head)

        if sym is not None:
            self.advance()
            return sym

        elif head.isdigit():
            return self.parse_natural_number()

        elif 'a' <= head <= 'z':
            self.advance()
            return LatinLetter(head)

        elif head == ' ':
            self.advance()
        else:
            raise self.error('Unexpected symbol')


class LambdaParser(Parser[LambdaToken]):
    def peek(self):
        while super().peek() == MiscToken.space:
            self.advance()

        return super().peek()

    def parse_variable(self):
        assert isinstance(self.peek(), LatinLetter)
        name = self.peek().value
        self.advance()

        if not self.is_at_end() and isinstance(self.peek(), NaturalNumber):
            name += self.peek().value
            self.advance()

        return Variable(name)

    def parse_abstraction(self):
        assert self.peek_multiple(2) == [MiscToken.left_parenthesis, MiscToken.l]
        start = self.index
        self.advance(2)

        if not isinstance(self.peek(), LatinLetter):
            raise self.error('Expected a variable name after "λ."', precede=self.index - start)

        var = self.parse_variable()

        if self.peek() == MiscToken.dot:
            self.advance()
        else:
            raise self.error('Expected dot after variable', precede=self.index - start)

        sub = self.parse_term()

        if self.is_at_end() or self.peek() != MiscToken.right_parenthesis:
            raise self.error('Unclosed parentheses for abstraction', precede=self.index - start)

        self.advance()
        return Abstraction(var, sub)

    def parse_application(self):
        assert self.peek() == MiscToken.left_parenthesis
        start = self.index
        self.advance()

        a = self.parse_term()

        if self.is_at_end():
            raise self.error('Unexpected end while parsing application', precede=self.index - start)

        b = self.parse_term()

        if self.is_at_end() or self.peek() != MiscToken.right_parenthesis:
            raise self.error('Unclosed parentheses for application', precede=self.index - start)

        self.advance()
        return Application(a, b)

    def parse_term(self):
        if isinstance(self.peek(), LatinLetter):
            return self.parse_variable()
        elif self.peek_multiple(2) == [MiscToken.left_parenthesis, MiscToken.l]:
            return self.parse_abstraction()
        elif self.peek() == MiscToken.left_parenthesis:
            return self.parse_application()
        else:
            raise self.error('Unexpected token')

    parse = parse_term


def parse_term(string: str):
    tokens = list(LambdaTokenizer(string).parse())
    parser = LambdaParser(tokens)
    term = parser.parse_term()

    if not parser.is_at_end():
        raise IncompleteMatchError(f'Did not match {repr(string)} in its entirety')

    return term
