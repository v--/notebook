
from ....parsing.identifiers import GreekIdentifier, LatinIdentifier
from ....parsing.mixins.whitespace import WhitespaceParserMixin
from ....parsing.parser import Parser
from ...fol.alphabet import BinaryConnective, PropConstant, Quantifier, UnaryConnective
from ...fol.terms import Variable
from ..markers import Marker
from ..rules import Premise, Rule
from ..schemas import (
    ConnectiveFormulaSchema,
    ConstantFormulaSchema,
    FormulaPlaceholder,
    FormulaSchema,
    NegationFormulaSchema,
    QuantifierFormulaSchema,
)
from .tokenizer import tokenize_nd_string
from .tokens import CapitalLatinString, MiscToken, RuleToken, SuperscriptToken


class NaturalDeductionParser(WhitespaceParserMixin[RuleToken], Parser[RuleToken]):
    def parse_variable(self) -> Variable:
        head = self.peek()
        assert isinstance(head, LatinIdentifier)
        self.advance()
        return Variable(head)

    def parse_marker(self) -> Marker:
        head = self.peek()
        assert isinstance(head, LatinIdentifier)
        self.advance()
        return Marker(head)

    def parse_placeholder(self) -> FormulaPlaceholder:
        head = self.peek()
        assert isinstance(head, GreekIdentifier)
        self.advance()
        return FormulaPlaceholder(head)

    def parse_constant_schema(self) -> ConstantFormulaSchema:
        head = self.peek()
        assert isinstance(head, PropConstant)
        self.advance()
        return ConstantFormulaSchema(head)

    def parse_binary_schema(self) -> ConnectiveFormulaSchema:
        start = self.index

        assert self.peek() == MiscToken.left_parenthesis
        self.advance()

        a_form = self.parse_schema()
        self.index - 1
        self.skip_spaces()

        if isinstance(connective := self.peek(), BinaryConnective):
            self.advance_and_skip_spaces()

            if not self.is_at_end() and self.peek() == MiscToken.right_parenthesis:
                raise self.error('Binary schemas must have a second sub-schema', i_first_token=start)
            if self.is_at_end():
                raise self.error('Unclosed parentheses for binary schema', i_first_token=start)

            b_form = self.parse_schema()
            self.index - 1

            if not self.is_at_end() and self.peek() == MiscToken.right_parenthesis:
                self.advance()
                return ConnectiveFormulaSchema(connective, a_form, b_form)

            raise self.error('Unclosed parentheses for binary schema', i_first_token=start, i_last_token=self.index - 1)

        raise self.error('Unexpected token')

    def parse_negation_schema(self) -> NegationFormulaSchema:
        assert self.peek() == UnaryConnective.negation
        self.advance()
        return NegationFormulaSchema(self.parse_schema())

    def parse_quantifier_schema(self) -> QuantifierFormulaSchema:
        q = self.peek()
        assert isinstance(q, Quantifier)

        start = self.index
        self.advance()

        if self.is_at_end() or not isinstance(self.peek(), LatinIdentifier):
            raise self.error('Expected a variable after the quantifier', i_first_token=start)

        var = self.parse_variable()

        if not self.is_at_end() and self.peek() == MiscToken.dot:
            self.advance()
        else:
            raise self.error('Expected dot after variable', i_first_token=start)

        return QuantifierFormulaSchema(q, var, self.parse_schema())

    def parse_schema(self) -> FormulaSchema:
        match self.peek():
            case PropConstant():
                return self.parse_constant_schema()

            case Quantifier():
                return self.parse_quantifier_schema()

            case MiscToken.left_parenthesis:
                return self.parse_binary_schema()

            case UnaryConnective.negation:
                return self.parse_negation_schema()

            case GreekIdentifier():
                return self.parse_placeholder()

            case _:
                raise self.error('Unexpected token')

    def parse_premise(self) -> Premise:
        discharge: FormulaSchema | None = None
        start = self.index

        if self.peek() == MiscToken.left_bracket:
            self.advance()

            discharge = self.parse_schema()

            if self.peek() == MiscToken.right_bracket:
                self.advance_and_skip_spaces()
            else:
                raise self.error('Unclosed brackets for discharge schemas', i_first_token=start)

        main = self.parse_schema()
        self.skip_spaces()
        return Premise(main, discharge)

    def parse_rule(self) -> Rule:
        start = self.index

        if self.peek() == MiscToken.left_parenthesis:
            self.advance()
        else:
            raise self.error('A rule must start with a parenthesized name')

        name: str = ''

        while isinstance(head := self.peek(), CapitalLatinString | PropConstant | UnaryConnective | BinaryConnective | Quantifier | SuperscriptToken):
            name += str(head)
            self.advance()

        if name == '':
            raise self.error('The name of a rule cannot be empty', i_first_token=start)

        if self.peek() == MiscToken.right_parenthesis:
            self.advance_and_skip_spaces()
        else:
            raise self.error('Unclosed parenthesis after rule name', i_first_token=start)

        premises = list[Premise]()

        while not self.is_at_end() and self.peek() != MiscToken.sequent_relation:
            premises.append(self.parse_premise())

            if self.is_at_end() or self.peek() == MiscToken.sequent_relation:
                continue

            if self.peek() == MiscToken.comma:
                self.advance_and_skip_spaces()
            else:
                raise self.error('Expected either a comma or a sequent symbol after a schema')

        if self.is_at_end():
            raise self.error('Expected a sequent symbol')

        self.advance_and_skip_spaces()
        c_start = self.index
        conclusion = self.parse_premise()

        if conclusion.discharge is not None:
            raise self.error('The conclusion cannot have a discharge schema', i_first_token=c_start)

        return Rule(name, premises, conclusion.main)


def parse_placeholder(string: str) -> FormulaPlaceholder:
    tokens = tokenize_nd_string(string)

    with NaturalDeductionParser(tokens) as parser:
        return parser.parse_placeholder()


def parse_schema(string: str) -> FormulaSchema:
    tokens = tokenize_nd_string(string)

    with NaturalDeductionParser(tokens) as parser:
        return parser.parse_schema()


def parse_marker(string: str) -> Marker:
    tokens = tokenize_nd_string(string)

    with NaturalDeductionParser(tokens) as parser:
        return parser.parse_marker()


def parse_rule(string: str) -> Rule:
    tokens = tokenize_nd_string(string)

    with NaturalDeductionParser(tokens) as parser:
        return parser.parse_rule()
