from ....parsing.identifiers import GreekIdentifier, LatinIdentifier
from ....parsing.mixins.whitespace import WhitespaceParserMixin
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


class NaturalDeductionParser(WhitespaceParserMixin[RuleToken], Parser[RuleToken]):
    def parse_variable(self) -> Variable:
        head = self.peek()
        assert isinstance(head, GreekIdentifier)
        self.advance()
        return Variable(head.value)

    def parse_atomic_placeholder(self) -> AtomicFormulaPlaceholder:
        head = self.peek()
        assert isinstance(head, GreekIdentifier)
        self.advance()
        return AtomicFormulaPlaceholder(head.value)

    def parse_constant_placeholder(self) -> ConstantFormulaPlaceholder:
        head = self.peek()
        assert isinstance(head, PropConstant)
        self.advance()
        return ConstantFormulaPlaceholder(head)

    def parse_binary_placeholder(self) -> ConnectiveFormulaPlaceholder:
        start = self.index

        assert self.peek() == MiscToken.left_parenthesis
        self.advance()

        a_form = self.parse_placeholder()
        self.index - 1
        self.skip_spaces()

        if isinstance(connective := self.peek(), BinaryConnective):
            self.advance_and_skip_spaces()

            if not self.is_at_end() and self.peek() == MiscToken.right_parenthesis:
                raise self.error('Binary placeholders must have a second sub-placeholder', i_first_token=start)
            if self.is_at_end():
                raise self.error('Unclosed parentheses for binary placeholder', i_first_token=start)

            b_form = self.parse_placeholder()
            self.index - 1

            if not self.is_at_end() and self.peek() == MiscToken.right_parenthesis:
                self.advance()
                return ConnectiveFormulaPlaceholder(connective, a_form, b_form)

            raise self.error('Unclosed parentheses for binary placeholder', i_first_token=start, i_last_token=self.index - 1)

        raise self.error('Unexpected token')

    def parse_negation_placeholder(self) -> NegationFormulaPlaceholder:
        assert self.peek() == MiscToken.negation
        self.advance()
        return NegationFormulaPlaceholder(self.parse_placeholder())

    def parse_quantifier_placeholder(self) -> QuantifierFormulaPlaceholder:
        q = self.peek()
        assert isinstance(q, Quantifier)

        start = self.index
        self.advance()

        if self.is_at_end() or not isinstance(self.peek(), GreekIdentifier):
            raise self.error('Expected a variable after the quantifier', i_first_token=start)

        var = self.parse_variable()

        if not self.is_at_end() and self.peek() == MiscToken.dot:
            self.advance()
        else:
            raise self.error('Expected dot after variable', i_first_token=start)

        return QuantifierFormulaPlaceholder(q, var, self.parse_placeholder())

    def parse_placeholder(self) -> FormulaPlaceholder:
        match self.peek():
            case PropConstant():
                return self.parse_constant_placeholder()

            case Quantifier():
                return self.parse_quantifier_placeholder()

            case MiscToken.left_parenthesis:
                return self.parse_binary_placeholder()

            case MiscToken.negation:
                return self.parse_negation_placeholder()

            case GreekIdentifier():
                return self.parse_atomic_placeholder()

            case _:
                raise self.error('Unexpected token')

    def parse_premise(self) -> Premise:
        discharge: FormulaPlaceholder | None = None
        start = self.index

        if self.peek() == MiscToken.left_bracket:
            self.advance()

            discharge = self.parse_placeholder()

            if self.peek() == MiscToken.right_bracket:
                self.advance_and_skip_spaces()
            else:
                raise self.error('Unclosed brackets for discharge placeholders', i_first_token=start)

        main = self.parse_placeholder()
        self.skip_spaces()
        return Premise(main, discharge)

    def parse_rule(self) -> Rule:
        start = self.index

        if self.peek() == MiscToken.left_parenthesis:
            self.advance()
        else:
            raise self.error('A rule must start with a parenthesized name')

        if isinstance(head := self.peek(), LatinIdentifier):
            name = head.value
            self.advance()
        else:
            raise self.error('The name of a rule must be a Latin identifier', i_first_token=start)

        if self.peek() == MiscToken.right_parenthesis:
            self.advance_and_skip_spaces()
        else:
            raise self.error('Unclosed parenthesis after rule name', i_first_token=start)

        premises: list[Premise] = []

        while not self.is_at_end() and self.peek() != MiscToken.sequent_relation:
            premises.append(self.parse_premise())

            if self.is_at_end() or self.peek() == MiscToken.sequent_relation:
                continue

            if self.peek() == MiscToken.comma:
                self.advance_and_skip_spaces()
            else:
                raise self.error('Expected either a comma or a sequent symbol after a placeholder')

        if self.is_at_end():
            raise self.error('Expected a sequent symbol')

        self.advance_and_skip_spaces()
        c_start = self.index
        conclusion = self.parse_premise()

        if conclusion.discharge is not None:
            raise self.error('The conclusion cannot have a discharge placeholder', i_first_token=c_start)

        return Rule(name, premises, conclusion.main)


def parse_rule(string: str) -> Rule:
    tokens = list(NaturalDeductionTokenizer(string).parse())
    parser = NaturalDeductionParser(tokens)
    rule = parser.parse_rule()
    parser.assert_exhausted()
    return rule
