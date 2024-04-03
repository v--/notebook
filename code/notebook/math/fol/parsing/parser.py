from typing import Iterable

from ....parsing.identifiers import GreekIdentifier, LatinIdentifier
from ....parsing.mixins.whitespace import WhitespaceParserMixin
from ....parsing.parser import Parser
from ..alphabet import BinaryConnective, PropConstant, Quantifier
from ..formulas import (
    ConnectiveFormula,
    ConstantFormula,
    EqualityFormula,
    Formula,
    NegationFormula,
    PredicateFormula,
    QuantifierFormula,
)
from ..terms import FunctionTerm, Term, Variable
from .tokenizer import FOLTokenizer
from .tokens import FOLToken, MiscToken


class FOLParser(WhitespaceParserMixin[FOLToken], Parser[FOLToken]):
    def parse_variable(self) -> Variable:
        head = self.peek()
        assert isinstance(head, GreekIdentifier)
        self.advance()
        return Variable(head.value)

    def parse_args(self) -> Iterable[Term]:
        assert self.peek() == MiscToken.left_parenthesis
        start = self.index
        self.advance_and_skip_spaces()

        if not self.is_at_end() and self.peek() == MiscToken.right_parenthesis:
            raise self.error('Empty argument list disallowed', i_first_token=start)

        while not self.is_at_end() and self.peek() != MiscToken.right_parenthesis:
            yield self.parse_term()

            if self.is_at_end():
                raise self.error('Unclosed argument list', i_first_token=start)

            if self.peek() == MiscToken.comma:
                self.advance_and_skip_spaces()
            elif self.peek() != MiscToken.right_parenthesis:
                raise self.error('Unexpected token')

        if self.is_at_end():
            raise self.error('Unclosed argument list', i_first_token=start)

        if self.peek() == MiscToken.right_parenthesis:
            self.advance()

    def parse_function(self) -> FunctionTerm:
        assert isinstance(self.peek(), LatinIdentifier)
        name = self.peek().value
        self.advance()

        if not self.is_at_end() and self.peek() == MiscToken.left_parenthesis:
            return FunctionTerm(name, list(self.parse_args()))

        return FunctionTerm(name, [])

    def parse_term(self) -> Term:
        match self.peek():
            case GreekIdentifier():
                return self.parse_variable()

            case LatinIdentifier():
                return self.parse_function()

            case _:
                raise self.error('Unexpected token')

    def parse_constant_formula(self) -> ConstantFormula:
        head = self.peek()
        assert isinstance(head, PropConstant)
        self.advance()
        return ConstantFormula(head)

    def parse_binary_formula(self) -> EqualityFormula | ConnectiveFormula:  # noqa: PLR0912
        start = self.index

        assert self.peek() == MiscToken.left_parenthesis
        self.advance()

        a_start = self.index
        a_term: Term | None = None
        a_form: Formula | None = None

        if isinstance(self.peek(), (GreekIdentifier, LatinIdentifier)):
            # We later correct it to a predicate formula if necessary
            a_term = self.parse_term()
        else:
            a_form = self.parse_formula()

        a_end = self.index - 1
        self.skip_spaces()

        if self.peek() == MiscToken.equality:
            if a_term is None:
                raise self.error('The left side of an equality formula must be a term', i_first_token=a_start, i_last_token=a_end)

            self.advance_and_skip_spaces()

            if not self.is_at_end() and self.peek() == MiscToken.right_parenthesis:
                raise self.error('Equality formulas must have a second term', i_first_token=start)

            if self.is_at_end():
                raise self.error('Unclosed parentheses for equality formula', i_first_token=start)

            b_term = self.parse_term()

            if not self.is_at_end() and self.peek() == MiscToken.right_parenthesis:
                self.advance()
                return EqualityFormula(a_term, b_term)

            raise self.error('Unclosed parentheses for equality formula', i_first_token=start, i_last_token=self.index - 1)

        if isinstance(connective := self.peek(), BinaryConnective):
            if isinstance(a_term, FunctionTerm):
                a_form = PredicateFormula(a_term.name, a_term.arguments)

            if a_form is None:
                raise self.error('The left side of a binary formula must be a formula', i_first_token=a_start, i_last_token=a_end)

            self.advance_and_skip_spaces()

            if not self.is_at_end() and self.peek() == MiscToken.right_parenthesis:
                raise self.error('Binary formulas must have a second subformula', i_first_token=start)

            if self.is_at_end():
                raise self.error('Unclosed parentheses for binary formula', i_first_token=start)

            b_form = self.parse_formula()
            self.index - 1

            if not self.is_at_end() and self.peek() == MiscToken.right_parenthesis:
                self.advance()
                return ConnectiveFormula(connective, a_form, b_form)

            raise self.error('Unclosed parentheses for binary formula', i_first_token=start, i_last_token=self.index - 1)

        raise self.error('Unexpected token')

    def parse_negation_formula(self) -> NegationFormula:
        assert self.peek() == MiscToken.negation
        self.advance()
        return NegationFormula(self.parse_formula())

    def parse_quantifier_formula(self) -> QuantifierFormula:
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

        return QuantifierFormula(q, var, self.parse_formula())

    def parse_predicate(self) -> PredicateFormula:
        assert isinstance(self.peek(), LatinIdentifier)
        name = self.peek().value
        self.advance()

        if not self.is_at_end() and self.peek() == MiscToken.left_parenthesis:
            return PredicateFormula(name, list(self.parse_args()))

        return PredicateFormula(name, [])

    def parse_formula(self) -> Formula:
        match self.peek():
            case PropConstant():
                return self.parse_constant_formula()

            case Quantifier():
                return self.parse_quantifier_formula()

            case MiscToken.left_parenthesis:
                return self.parse_binary_formula()

            case MiscToken.negation:
                return self.parse_negation_formula()

            case LatinIdentifier():
                return self.parse_predicate()

            case _:
                raise self.error('Unexpected token')


def parse_term(string: str) -> Term:
    tokens = list(FOLTokenizer(string).parse())
    parser = FOLParser(tokens)
    term = parser.parse_term()
    parser.assert_exhausted()
    return term


def parse_formula(string: str) -> Formula:
    tokens = list(FOLTokenizer(string).parse())
    parser = FOLParser(tokens)
    formula = parser.parse_formula()
    parser.assert_exhausted()
    return formula
