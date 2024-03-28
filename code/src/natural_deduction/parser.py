from typing import Iterable

from ..support.parsing.parser import Parser, ParserError

from .tokens import RuleToken, MiscToken, LatinName, GreekName, NaturalNumber
from .rules import AtomicFormulaPlaceholder, ConstantFormulaPlaceholder, NegationFormulaPlaceholder, ConnectiveFormulaPlaceholder, QuantifierFormulaPlaceholder, FormulaPlaceholder, Premise, Rule
from ..fol.terms import Variable
from ..fol.tokens import PropConstant, BinaryConnective, Quantifier


class IncompleteMatchError(ParserError):
    pass


class NaturalDeductionTokenizer(Parser[str]):
    def take_while_in_range(self, start: str, end: str):
        buffer: list[str] = []

        while not self.is_at_end() and start <= self.peek() <= end:
            buffer.append(self.peek())
            self.advance()

        assert len(buffer) > 0
        return ''.join(buffer)

    def parse(self) -> Iterable[RuleToken]:
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

        if head == '₀':
            raise self.error('Natural numbers cannot start with zero')

        elif head.isdigit():
            return NaturalNumber(self.take_while_in_range('₀', '₉'))

        elif 'A' <= head <= 'Z':
            return LatinName(self.take_while_in_range('A', 'Z'))

        elif 'a' <= head <= 'z':
            return LatinName(self.take_while_in_range('a', 'z'))

        elif 'Α' <= head <= 'Ω':
            return GreekName(self.take_while_in_range('Α', 'Ω'))

        elif 'α' <= head <= 'ω':
            return GreekName(self.take_while_in_range('α', 'ω'))

        elif head == ' ':
            self.advance()
        else:
            raise self.error('Unexpected symbol')


class NaturalDeductionParser(Parser[RuleToken]):
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

    def parse_atomic(self):
        assert isinstance(self.peek(), GreekName)
        name = self.peek().value
        self.advance()

        if not self.is_at_end() and isinstance(self.peek(), NaturalNumber):
            name += self.peek().value
            self.advance()

        return AtomicFormulaPlaceholder(name)

    def parse_constant_formula(self):
        value = PropConstant.try_match(self.peek())
        assert value is not None
        self.advance()
        return ConstantFormulaPlaceholder(value)

    def parse_binary_placeholder(self):
        assert self.peek() == MiscToken.left_parenthesis
        self.advance()
        a_start = self.index

        if isinstance(self.peek(), GreekName):
            a = self.parse_placeholder()
        else:
            raise self.error('Expected a formula placeholder', precede=self.index - a_start)

        if BinaryConnective.try_match(self.peek()):
            connective = self.peek()

            if isinstance(a, FormulaPlaceholder):  # type: ignore
                self.advance()
                b = self.parse_placeholder()

                if self.peek() == MiscToken.right_parenthesis:
                    self.advance()
                    return ConnectiveFormulaPlaceholder(connective, a, b)
                else:
                    raise self.error('Unclosed parentheses for binary formula placeholder', precede=self.index - a_start)
            else:
                raise self.error('The left side of a connective formula placeholder must itself be a placeholder', precede=self.index - a_start)

        else:
            raise self.error('Unexpected token')

    def parse_negation_placeholder(self):
        assert self.peek() == MiscToken.negation
        self.advance()
        return NegationFormulaPlaceholder(self.parse_placeholder())

    def parse_quantifier_placeholder(self):
        assert Quantifier.try_match(self.peek())
        q = self.peek()
        self.advance()
        var = self.parse_variable()

        if self.peek() == MiscToken.dot:
            self.advance()
        else:
            raise self.error('Expected dot after variable')

        return QuantifierFormulaPlaceholder(q, var, self.parse_placeholder())

    def parse_placeholder(self):
        match self.peek():
            case _ if PropConstant.try_match(self.peek()):
                return self.parse_constant_formula()

            case _ if Quantifier.try_match(self.peek()):
                return self.parse_quantifier_placeholder()

            case MiscToken.left_parenthesis:
                return self.parse_binary_placeholder()

            case MiscToken.negation:
                return self.parse_negation_placeholder()

            case GreekName():
                return self.parse_atomic()

            case _:
                raise self.error('Unexpected token')

    def parse_premise(self):
        discharge: FormulaPlaceholder | None = None

        if self.peek() == MiscToken.left_bracket:
            self.advance()

            discharge = self.parse_placeholder()

            if self.peek() == MiscToken.right_bracket:
                self.advance()
            else:
                raise self.error('Brackets for discharge formulas must be closed')

        main = self.parse_placeholder()
        return Premise(main, discharge)

    def parse_rule(self):
        if self.peek() == MiscToken.left_parenthesis:
            self.advance()
        else:
            raise self.error('A rule must start with an opening parenthesis')

        if isinstance(self.peek(), LatinName):
            name = self.peek()
            self.advance()
        else:
            raise self.error('The name of a rule must be a Latin identifier')

        if self.peek() == MiscToken.right_parenthesis:
            self.advance()
        else:
            raise self.error('A rule must have a closing parenthesis after its name')

        premises: list[Premise] = []

        while self.peek() != MiscToken.sequent_relation:
            premises.append(self.parse_premise())

            if self.peek() == MiscToken.sequent_relation:
                continue
            if self.peek() == MiscToken.comma:
                self.advance()
            else:
                raise self.error('Expected either a comma a sequent symbol after a formula placeholder')

        if self.peek() == MiscToken.sequent_relation:
            self.advance()
        else:
            raise self.error('Expected a sequent symbol')

        conclusion = self.parse_placeholder()
        return Rule(name, premises, conclusion)

    parse = parse_rule


def parse_rule(string: str):
    tokens = list(NaturalDeductionTokenizer(string).parse())
    parser = NaturalDeductionParser(tokens)
    formula = parser.parse_rule()

    if not parser.is_at_end():
        raise IncompleteMatchError(f'Did not match {repr(string)} in its entirety')

    return formula
