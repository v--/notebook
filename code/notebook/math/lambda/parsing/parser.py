from ....parsing.identifiers import LatinIdentifier
from ....parsing.parser import Parser
from ..terms import Abstraction, Application, Variable
from .tokenizer import LambdaTokenizer
from .tokens import LambdaToken, MiscToken


class LambdaParser(Parser[LambdaToken]):
    def parse_variable(self) -> Variable:
        head = self.peek()
        assert isinstance(head, LatinIdentifier)
        self.advance()
        return Variable(head.value)

    def parse_abstraction(self):
        assert self.peek_multiple(2) == [MiscToken.left_parenthesis, MiscToken.l]
        start = self.index
        self.advance(2)

        if self.is_at_end() or not isinstance(self.peek(), LatinIdentifier):
            raise self.error('Expected a variable name after λ', i_first_token=start)

        var = self.parse_variable()

        if self.peek() == MiscToken.dot:
            self.advance()
        else:
            raise self.error('Expected a dot after an abstraction variable', i_first_token=start)

        sub = self.parse_term()

        if self.is_at_end() or self.peek() != MiscToken.right_parenthesis:
            raise self.error('Unclosed parentheses for abstraction', i_first_token=start)

        self.advance()
        return Abstraction(var, sub)

    def parse_application(self):
        assert self.peek() == MiscToken.left_parenthesis
        start = self.index
        self.advance()

        a = self.parse_term()

        if self.is_at_end() or self.peek() == MiscToken.right_parenthesis:
            raise self.error('Applications must have a second subterm', i_first_token=start)

        b = self.parse_term()

        if self.is_at_end() or self.peek() != MiscToken.right_parenthesis:
            raise self.error('Unclosed parentheses for application', i_first_token=start)

        self.advance()
        return Application(a, b)

    def parse_term(self):
        if isinstance(self.peek(), LatinIdentifier):
            return self.parse_variable()
        elif self.peek_multiple(2) == [MiscToken.left_parenthesis, MiscToken.right_parenthesis]:
            raise self.error('Applications must have two terms, while abstractions must begin with λ', i_last_token=self.index + 1)
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
