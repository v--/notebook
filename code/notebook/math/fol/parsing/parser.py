from dataclasses import dataclass
from typing import Iterable

from ....parsing.identifiers import LatinIdentifier
from ....parsing.mixins.whitespace import WhitespaceParserMixin
from ....parsing.parser import Parser
from ..alphabet import BinaryConnective, PropConstant, Quantifier, UnaryConnective
from ..formulas import (
    ConnectiveFormula,
    ConstantFormula,
    EqualityFormula,
    Formula,
    NegationFormula,
    PredicateFormula,
    QuantifierFormula,
)
from ..propositional import propositional_signature
from ..signature import FOLSignature
from ..terms import FunctionTerm, Term, Variable
from .tokenizer import tokenize_fol_string
from .tokens import FOLToken, FunctionSymbolToken, MiscToken, PredicateSymbolToken


@dataclass
class FOLParser(WhitespaceParserMixin[FOLToken], Parser[FOLToken]):
    signature: FOLSignature

    def parse_variable(self) -> Variable:
        head = self.peek()
        assert isinstance(head, LatinIdentifier)
        self.advance()
        return Variable(head)

    def parse_args(self, arity: int, i_start: int) -> Iterable[Term]:
        assert self.peek() == MiscToken.left_parenthesis
        self.advance_and_skip_spaces()

        if not self.is_at_end() and self.peek() == MiscToken.right_parenthesis:
            if arity == 0:
                raise self.error('Avoid the argument list at all when zero arguments are expected', i_first_token=i_start)

            raise self.error('Empty argument lists are disallowed', i_first_token=i_start)

        while True:
            if self.is_at_end():
                raise self.error('Unclosed argument list', i_first_token=i_start)

            if self.peek() == MiscToken.right_parenthesis:
                raise self.error('Unexpected closing parenthesis for argument list', i_first_token=i_start)

            yield self.parse_term()

            if self.is_at_end():
                raise self.error('Unclosed argument list', i_first_token=i_start)

            if self.peek() == MiscToken.comma:
                self.advance_and_skip_spaces()
            elif self.peek() == MiscToken.right_parenthesis:
                self.advance()
                return
            else:
                raise self.error('Unexpected token')

    def _parse_function_like(self, arity: int) -> tuple[str, list[Term]]:
        i_start = self.index
        name = self.peek().value
        self.advance()

        arguments: list[Term] = []

        if not self.is_at_end() and self.peek() == MiscToken.left_parenthesis:
            arguments = list(self.parse_args(arity, i_start))

        if arity != len(arguments):
            raise self.error(f'Expected {arity} arguments for {name} but got {len(arguments)}', i_first_token=i_start)

        return (name, arguments)

    def parse_term(self) -> Term:
        match self.peek():
            case LatinIdentifier():
                return self.parse_variable()

            case FunctionSymbolToken():
                arity = self.signature.get_function_arity(str(self.peek()))
                return FunctionTerm(*self._parse_function_like(arity))

        raise self.error('Unexpected token')

    def parse_constant_formula(self) -> ConstantFormula:
        head = self.peek()
        assert isinstance(head, PropConstant)
        self.advance()
        return ConstantFormula(head)

    def parse_binary_formula(self) -> EqualityFormula | ConnectiveFormula:  # noqa: PLR0912
        i_start = self.index

        assert self.peek() == MiscToken.left_parenthesis
        self.advance()

        i_a_start = self.index
        a_term: Term | None = None
        a_form: Formula | None = None

        if isinstance(self.peek(), (LatinIdentifier, FunctionSymbolToken)):
            a_term = self.parse_term()
        else:
            a_form = self.parse_formula()

        i_a_end = self.index - 1
        self.skip_spaces()

        if self.peek() == MiscToken.equality:
            if a_term is None:
                raise self.error('The left side of an equality formula must be a term', i_first_token=i_a_start, i_last_token=i_a_end)

            self.advance_and_skip_spaces()

            if not self.is_at_end() and self.peek() == MiscToken.right_parenthesis:
                raise self.error('Equality formulas must have a second term', i_first_token=i_start)

            if self.is_at_end():
                raise self.error('Unclosed parentheses for equality formula', i_first_token=i_start)

            b_term = self.parse_term()

            if not self.is_at_end() and self.peek() == MiscToken.right_parenthesis:
                self.advance()
                return EqualityFormula(a_term, b_term)

            raise self.error('Unclosed parentheses for equality formula', i_first_token=i_start, i_last_token=self.index - 1)

        if isinstance(connective := self.peek(), BinaryConnective):
            if isinstance(a_term, FunctionTerm):
                a_form = PredicateFormula(a_term.name, a_term.arguments)

            if a_form is None:
                raise self.error('The left side of a binary formula must be a formula', i_first_token=i_a_start, i_last_token=i_a_end)

            self.advance_and_skip_spaces()

            if not self.is_at_end() and self.peek() == MiscToken.right_parenthesis:
                raise self.error('Binary formulas must have a second subformula', i_first_token=i_start)

            if self.is_at_end():
                raise self.error('Unclosed parentheses for binary formula', i_first_token=i_start)

            b_form = self.parse_formula()
            self.index - 1

            if not self.is_at_end() and self.peek() == MiscToken.right_parenthesis:
                self.advance()
                return ConnectiveFormula(connective, a_form, b_form)

            raise self.error('Unclosed parentheses for binary formula', i_first_token=i_start, i_last_token=self.index - 1)

        raise self.error('Unexpected token')

    def parse_negation_formula(self) -> NegationFormula:
        assert self.peek() == UnaryConnective.negation
        self.advance()
        return NegationFormula(self.parse_formula())

    def parse_quantifier_formula(self) -> QuantifierFormula:
        q = self.peek()
        assert isinstance(q, Quantifier)

        i_start = self.index
        self.advance()

        if self.is_at_end() or not isinstance(self.peek(), LatinIdentifier):
            raise self.error('Expected a variable after the quantifier', i_first_token=i_start)

        var = self.parse_variable()

        if not self.is_at_end() and self.peek() == MiscToken.dot:
            self.advance()
        else:
            raise self.error('Expected dot after variable', i_first_token=i_start)

        return QuantifierFormula(q, var, self.parse_formula())

    def parse_formula(self) -> Formula:
        match self.peek():
            case PropConstant():
                return self.parse_constant_formula()

            case Quantifier():
                return self.parse_quantifier_formula()

            case MiscToken.left_parenthesis:
                return self.parse_binary_formula()

            case UnaryConnective.negation:
                return self.parse_negation_formula()

            case PredicateSymbolToken():
                arity = self.signature.get_predicate_arity(str(self.peek()))
                return PredicateFormula(*self._parse_function_like(arity))

            case _:
                raise self.error('Unexpected token')


def parse_term(signature: FOLSignature, string: str) -> Term:
    tokens = tokenize_fol_string(signature, string)

    with FOLParser(tokens, signature) as parser:
        return parser.parse_term()


def parse_formula(signature: FOLSignature, string: str) -> Formula:
    tokens = tokenize_fol_string(signature, string)

    with FOLParser(tokens, signature) as parser:
        return parser.parse_formula()


def parse_propositional_formula(string: str) -> Formula:
    return parse_formula(propositional_signature, string)
