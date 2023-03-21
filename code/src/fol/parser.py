from typing import Iterable

from ..support.parsing import Parser

from .tokens import BinaryConnective, FOLToken, GreekName, LatinName, MiscToken, NaturalNumber, PropConstant, Quantifier

from .terms import Variable, FunctionTerm, Term
from .formulas import ConnectiveFormula, EqualityFormula, NegationFormula, PredicateFormula, QuantifierFormula, Formula


class FOLTokenizer(Parser[str]):
    def take_while_in_range(self, start: str, end: str):
        buffer: list[str] = []

        while not self.is_at_end() and start <= self.peek() <= end:
            buffer.append(self.peek())
            self.advance()

        assert len(buffer) > 0
        return ''.join(buffer)

    def parse(self) -> Iterable[FOLToken]:
        while not self.is_at_end():
            yield self.parse_step(self.peek())

    def parse_step(self, head: str):
        sym = PropConstant.try_match(head) or \
            BinaryConnective.try_match(head) or \
            Quantifier.try_match(head) or \
            MiscToken.try_match(head)

        if sym is not None:
            self.advance()
            return sym

        if head == '0':
            raise self.error('Natural numbers cannot start with zero')

        elif head.isdigit():
            return NaturalNumber(self.take_while_in_range('0', '9'))

        elif 'a' <= head <= 'z':
            return LatinName(self.take_while_in_range('a', 'z'))

        elif 'α' <= head <= 'ω':
            return GreekName(self.take_while_in_range('α', 'ω'))

        elif head == ' ':
            self.advance()
        else:
            raise self.error('Unexpected symbol')


class FOLParser(Parser[FOLToken]):
    def peek(self):
        while super().peek() == MiscToken.space:
            self.advance()

        return super().peek()

    def parse_variable(self):
        assert isinstance(self.peek(), GreekName)
        name = self.peek().value
        self.advance()

        if not self.is_at_end() and isinstance(self.peek(), NaturalNumber):
            name += self.peek().value
            self.advance()

        return Variable(name)

    def parse_args(self):
        assert self.peek() == MiscToken.left_parenthesis
        self.advance()

        if self.peek() == MiscToken.right_parenthesis:
            raise self.error('Empty argument list disallowed')

        while self.peek() != MiscToken.right_parenthesis:
            yield self.parse_term()

            if self.peek() == MiscToken.comma:
                self.advance()
            elif self.peek() != MiscToken.right_parenthesis:
                raise self.error('Unexpected token')

        if self.peek() == MiscToken.right_parenthesis:
            self.advance()

    def parse_function(self):
        assert isinstance(self.peek(), LatinName)
        name = self.peek().value
        self.advance()

        if self.is_at_end():
            return FunctionTerm(name, [])

        if isinstance(self.peek(), NaturalNumber):
            name += self.peek().value
            self.advance()

        if not self.is_at_end() and self.peek() == MiscToken.left_parenthesis:
            return FunctionTerm(name, list(self.parse_args()))

        return FunctionTerm(name, [])

    def parse_term(self):
        match self.peek():
            case GreekName():
                return self.parse_variable()

            case LatinName():
                return self.parse_function()

            case _:
                raise self.error('Unexpected token')

    def parse_binary_formula(self):
        assert self.peek() == MiscToken.left_parenthesis
        self.advance()
        a_start = self.index

        if isinstance(self.peek(), (GreekName, LatinName)):
            # We later correct it to a predicate formula if necessary
            a = self.parse_term()
        else:
            a = self.parse_formula()

        if self.peek() == MiscToken.equality:
            if isinstance(a, Term):  # type: ignore
                self.advance()
                b = self.parse_term()

                if self.peek() == MiscToken.right_parenthesis:
                    self.advance()
                    return EqualityFormula(a, b)
                else:
                    raise self.error('Unclosed parentheses for binary formula', precede=self.index - a_start)
            else:
                raise self.error('The left side of an MiscToken.equality formula must be a term', precede=self.index - a_start)

        elif BinaryConnective.try_match(self.peek()):
            connective = self.peek()

            if isinstance(a, FunctionTerm) and len(a.arguments) > 0:
                a = PredicateFormula(a.name, a.arguments)

            if isinstance(a, Formula):  # type: ignore
                self.advance()
                b = self.parse_formula()

                if self.peek() == MiscToken.right_parenthesis:
                    self.advance()
                    return ConnectiveFormula(connective, a, b)
                else:
                    raise self.error('Unclosed parentheses for binary formula', precede=self.index - a_start)
            else:
                raise self.error('The left side of an MiscToken.equality formula must be a formula', precede=self.index - a_start)

        else:
            raise self.error('Unexpected token')

    def parse_negation_formula(self):
        assert self.peek() == MiscToken.negation
        self.advance()
        return NegationFormula(self.parse_formula())

    def parse_quantifier_formula(self):
        assert Quantifier.try_match(self.peek())
        q = self.peek()
        self.advance()
        var = self.parse_variable()

        if self.peek() == MiscToken.dot:
            self.advance()
        else:
            raise self.error('Expected dot after variable')

        return QuantifierFormula(q, var, self.parse_formula())

    def parse_predicate(self):
        assert isinstance(self.peek(), LatinName)
        name = self.peek().value
        self.advance()

        if self.is_at_end():
            raise self.error('Predicates must have parameters')
        elif isinstance(self.peek(), NaturalNumber):
            name += self.peek().value
            self.advance()

        if self.is_at_end():
            raise self.error('Predicates must have parameters')
        elif self.peek() == MiscToken.left_parenthesis:
            return PredicateFormula(name, list(self.parse_args()))

        return PredicateFormula(name, [])

    def parse_formula(self):
        match self.peek():
            case _ if Quantifier.try_match(self.peek()):
                return self.parse_quantifier_formula()

            case MiscToken.left_parenthesis:
                return self.parse_binary_formula()

            case MiscToken.negation:
                return self.parse_negation_formula()

            case LatinName():
                return self.parse_predicate()

            case _:
                raise self.error('Unexpected token')

    parse = parse_formula


def parse_term(string: str):
    tokens = list(FOLTokenizer(string).parse())
    return FOLParser(tokens).parse_term()


def parse_formula(string: str):
    tokens = list(FOLTokenizer(string).parse())
    return FOLParser(tokens).parse_formula()
