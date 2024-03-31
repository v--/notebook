from ....parsing.identifiers import GreekIdentifier, LatinIdentifier
from ....parsing.parser import Parser
from ...fol.alphabet import BinaryConnective, PropConstant, Quantifier
from ...fol.terms import Variable
from ..rules import (
    AtomicFormulaPlaceholder,
    ConnectiveFormulaPlaceholder,
    ConstantFormulaPlaceholder,
    FormulaPlaceholder,
    NegationFormulaPlaceholder,
    Premise,
    QuantifierFormulaPlaceholder,
    Rule,
)
from .tokenizer import NaturalDeductionTokenizer
from .tokens import MiscToken, RuleToken


class NaturalDeductionParser(Parser[RuleToken]):
    def peek(self):
        while super().peek() == MiscToken.space:
            self.advance()

        return super().peek()

    def parse_variable(self):
        head = self.peek()
        assert isinstance(head, GreekIdentifier)
        self.advance()
        return Variable(head.value)

    def parse_atomic(self):
        head = self.peek()
        assert isinstance(head, GreekIdentifier)
        self.advance()
        return AtomicFormulaPlaceholder(head.value)

    def parse_constant_formula(self):
        head = self.peek()
        assert isinstance(head, PropConstant)
        self.advance()
        return ConstantFormulaPlaceholder(head)

    def parse_binary_placeholder(self):
        assert self.peek() == MiscToken.left_parenthesis
        self.advance()
        a_start = self.index

        if isinstance(self.peek(), GreekIdentifier):
            a = self.parse_placeholder()
        else:
            raise self.error('Expected a formula placeholder', precede=self.index - a_start)

        if isinstance(connective := self.peek(), BinaryConnective):
            # See https://github.com/python/mypy/issues/16707
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
        q = self.peek()
        assert isinstance(q, Quantifier)
        self.advance()
        var = self.parse_variable()

        if self.peek() == MiscToken.dot:
            self.advance()
        else:
            raise self.error('Expected dot after variable')

        return QuantifierFormulaPlaceholder(q, var, self.parse_placeholder())

    def parse_placeholder(self):
        match self.peek():
            case PropConstant():
                return self.parse_constant_formula()

            case Quantifier():
                return self.parse_quantifier_placeholder()

            case MiscToken.left_parenthesis:
                return self.parse_binary_placeholder()

            case MiscToken.negation:
                return self.parse_negation_placeholder()

            case GreekIdentifier():
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

        if isinstance(head := self.peek(), LatinIdentifier):
            name = head.value
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
    rule = parser.parse_rule()
    parser.assert_exhausted()
    return rule
