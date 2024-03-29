from ..support.parsing.parser import Parser
from ..support.parsing.identifiers import LatinIdentifier

from .tokens import LambdaToken, MiscToken
from .terms import Variable, Application, Abstraction
from .tokenizer import LambdaTokenizer


class LambdaParser(Parser[LambdaToken]):
    def peek(self):
        while super().peek() == MiscToken.space:
            self.advance()

        return super().peek()

    def parse_variable(self) -> Variable:
        head = self.peek()
        assert isinstance(head, LatinIdentifier)
        self.advance()
        return Variable(head.value)

    def parse_abstraction(self):
        assert self.peek_multiple(2) == [MiscToken.left_parenthesis, MiscToken.l]
        start = self.index
        self.advance(2)

        if not isinstance(self.peek(), LatinIdentifier):
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
        if isinstance(self.peek(), LatinIdentifier):
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
    parser.assert_exhausted()
    return term
