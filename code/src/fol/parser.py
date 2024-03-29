from typing import Iterable

from ..support.parsing.parser import Parser
from ..support.parsing.identifiers import LatinIdentifier, GreekIdentifier

from .tokens import BinaryConnective, FOLToken, MiscToken, PropConstant, Quantifier
from .terms import Variable, FunctionTerm, Term
from .formulas import ConstantFormula, ConnectiveFormula, EqualityFormula, NegationFormula, PredicateFormula, QuantifierFormula, Formula
from .tokenizer import FOLTokenizer


class FOLParser(Parser[FOLToken]):
    def peek(self):
        while super().peek() == MiscToken.space:
            self.advance()

        return super().peek()

    def parse_variable(self) -> Variable:
        head = self.peek()
        assert isinstance(head, GreekIdentifier)
        self.advance()
        return Variable(head.value)

    def parse_args(self) -> Iterable[Term]:
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

    def parse_binary_formula(self) -> EqualityFormula | ConnectiveFormula:
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

        if self.peek() == MiscToken.equality:
            if a_term is None:
                raise self.error('The left side of an equality formula must be a term', precede=self.index - a_start)

            self.advance()
            b_term = self.parse_term()

            if self.peek() == MiscToken.right_parenthesis:
                self.advance()
                return EqualityFormula(a_term, b_term)
            else:
                raise self.error('Unclosed parentheses for binary formula', precede=self.index - a_start)

        elif isinstance(connective := self.peek(), BinaryConnective):
            if isinstance(a_term, FunctionTerm):
                a_form = PredicateFormula(a_term.name, a_term.arguments)

            if a_form is None:
                raise self.error('The left side of a connective formula must be a formula', precede=self.index - a_start)

            self.advance()
            b_form = self.parse_formula()

            if self.peek() == MiscToken.right_parenthesis:
                self.advance()
                return ConnectiveFormula(connective, a_form, b_form)  # type: ignore
            else:
                raise self.error('Unclosed parentheses for binary formula', precede=self.index - a_start)

        else:
            raise self.error('Unexpected token')

    def parse_negation_formula(self) -> NegationFormula:
        assert self.peek() == MiscToken.negation
        self.advance()
        return NegationFormula(self.parse_formula())

    def parse_quantifier_formula(self) -> QuantifierFormula:
        q = self.peek()
        assert isinstance(q, Quantifier)
        self.advance()
        var = self.parse_variable()

        if self.peek() == MiscToken.dot:
            self.advance()
        else:
            raise self.error('Expected dot after variable')

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

    parse = parse_formula


def parse_term(string: str):
    tokens = list(FOLTokenizer(string).parse())
    parser = FOLParser(tokens)
    term = parser.parse_term()
    parser.assert_exhausted()
    return term


def parse_formula(string: str):
    tokens = list(FOLTokenizer(string).parse())
    parser = FOLParser(tokens)
    formula = parser.parse_formula()
    parser.assert_exhausted()
    return formula
