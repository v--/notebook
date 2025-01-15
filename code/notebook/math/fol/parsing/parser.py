from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import Literal, cast, overload

from ....parsing.identifiers import GreekIdentifier, LatinIdentifier
from ....parsing.mixins.inference_rules import InferenceRuleParserMixin
from ....parsing.mixins.whitespace import WhitespaceParserMixin
from ....parsing.parser import Parser
from ...stt.alphabet import RuleConnective
from ..alphabet import BinaryConnective, PropConstant, Quantifier, UnaryConnective
from ..deduction import Marker, NaturalDeductionPremise, NaturalDeductionRule
from ..formulas import (
    ConnectiveFormula,
    ConnectiveFormulaSchema,
    ConstantFormula,
    EqualityFormula,
    EqualityFormulaSchema,
    Formula,
    FormulaPlaceholder,
    FormulaSchema,
    NegationFormula,
    NegationFormulaSchema,
    PredicateFormula,
    QuantifierFormula,
    QuantifierFormulaSchema,
)
from ..propositional import propositional_signature
from ..signature import EMPTY_SIGNATURE, FOLSignature
from ..terms import FunctionTerm, Term, TermPlaceholder, TermSchema, Variable, VariablePlaceholder
from .tokenizer import tokenize_fol_string
from .tokens import FOLToken, FunctionSymbolToken, MiscToken, PredicateSymbolToken


@dataclass
class FOLParser(InferenceRuleParserMixin[FOLToken], WhitespaceParserMixin[FOLToken], Parser[FOLToken]):
    signature: FOLSignature

    def parse_term_placeholder(self) -> TermPlaceholder:
        head = self.peek()
        assert isinstance(head, GreekIdentifier)
        self.advance()
        return TermPlaceholder(head)

    def parse_formula_placeholder(self) -> FormulaPlaceholder:
        head = self.peek()
        assert isinstance(head, GreekIdentifier)
        self.advance()
        return FormulaPlaceholder(head)

    def parse_marker(self) -> Marker:
        head = self.peek()
        assert isinstance(head, LatinIdentifier)
        self.advance()
        return Marker(head)

    @overload
    def parse_variable(self, *, parse_schema: Literal[False]) -> Variable: ...
    @overload
    def parse_variable(self, *, parse_schema: Literal[True]) -> VariablePlaceholder: ...
    @overload
    def parse_variable(self, *, parse_schema: bool) -> Variable | VariablePlaceholder: ...
    def parse_variable(self, *, parse_schema: bool) -> Variable | VariablePlaceholder:
        head = self.peek()
        assert isinstance(head, LatinIdentifier)
        self.advance()

        if parse_schema:
            return VariablePlaceholder(head)

        return Variable(head)

    @overload
    def parse_args(self, arity: int, i_start: int, *, parse_schema: Literal[False]) -> Iterable[Term]: ...
    @overload
    def parse_args(self, arity: int, i_start: int, *, parse_schema: Literal[True]) -> Iterable[TermSchema]: ...
    @overload
    def parse_args(self, arity: int, i_start: int, *, parse_schema: bool) -> Iterable[Term] | Iterable[TermSchema]: ...
    def parse_args(self, arity: int, i_start: int, *, parse_schema: bool) -> Iterable[Term] | Iterable[TermSchema]:
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

            yield self.parse_term(parse_schema=parse_schema)

            if self.is_at_end():
                raise self.error('Unclosed argument list', i_first_token=i_start)

            if self.peek() == MiscToken.comma:
                self.advance_and_skip_spaces()
            elif self.peek() == MiscToken.right_parenthesis:
                self.advance()
                return
            else:
                raise self.error('Unexpected token')

    @overload
    def _parse_function_like(self, arity: int, *, parse_schema: Literal[False]) -> tuple[str, Sequence[Term]]: ...
    @overload
    def _parse_function_like(self, arity: int, *, parse_schema: Literal[True]) -> tuple[str, Sequence[TermSchema]]: ...
    @overload
    def _parse_function_like(self, arity: int, *, parse_schema: bool) -> tuple[str, Sequence[Term]] | tuple[str, Sequence[TermSchema]]: ...
    def _parse_function_like(self, arity: int, *, parse_schema: bool) -> tuple[str, Sequence[Term]] | tuple[str, Sequence[TermSchema]]:
        i_start = self.index
        name: str = self.peek().value
        self.advance()

        # A narrower type leads to duplicated code
        arguments = list[Term | TermSchema]()

        if not self.is_at_end() and self.peek() == MiscToken.left_parenthesis:
            arguments = list(self.parse_args(arity, i_start, parse_schema=parse_schema))

            if arity != len(arguments):
                raise self.error(f'Expected {arity} arguments for {name} but got {len(arguments)}', i_first_token=i_start)

        return cast(
            tuple[str, Sequence[Term]] | tuple[str, Sequence[TermSchema]],
            (name, arguments)
        )

    @overload
    def parse_term(self, *, parse_schema: Literal[False]) -> Term: ...
    @overload
    def parse_term(self, *, parse_schema: Literal[True]) -> TermSchema: ...
    @overload
    def parse_term(self, *, parse_schema: bool) -> Term | TermSchema: ...
    def parse_term(self, *, parse_schema: bool) -> Term | TermSchema:
        match self.peek():
            case LatinIdentifier():
                return self.parse_variable(parse_schema=parse_schema)

            case FunctionSymbolToken():
                arity = self.signature.get_function_arity(str(self.peek()))
                return FunctionTerm(*self._parse_function_like(arity, parse_schema=parse_schema))

        raise self.error('Unexpected token')

    def parse_constant_formula(self) -> ConstantFormula:
        head = self.peek()
        assert isinstance(head, PropConstant)
        self.advance()
        return ConstantFormula(head)

    @overload
    def parse_binary_formula(self, *, parse_schema: Literal[False]) -> EqualityFormula | ConnectiveFormula: ...
    @overload
    def parse_binary_formula(self, *, parse_schema: Literal[True]) -> EqualityFormulaSchema | ConnectiveFormulaSchema: ...
    @overload
    def parse_binary_formula(self, *, parse_schema: bool) -> EqualityFormula | EqualityFormulaSchema | ConnectiveFormula | ConnectiveFormulaSchema: ...
    def parse_binary_formula(self, *, parse_schema: bool) -> EqualityFormula | EqualityFormulaSchema | ConnectiveFormula | ConnectiveFormulaSchema:  # noqa: PLR0912
        i_start = self.index

        assert self.peek() == MiscToken.left_parenthesis
        self.advance()

        i_a_start = self.index
        a_term: Term | TermSchema | None = None
        a_form: Formula | FormulaSchema | None = None

        if isinstance(self.peek(), LatinIdentifier | FunctionSymbolToken):
            a_term = self.parse_term(parse_schema=parse_schema)
        else:
            a_form = self.parse_formula(parse_schema=parse_schema)

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

            b_term = self.parse_term(parse_schema=parse_schema)

            if not self.is_at_end() and self.peek() == MiscToken.right_parenthesis:
                self.advance()

                if parse_schema:
                    assert isinstance(a_term, TermSchema)
                    assert isinstance(b_term, TermSchema)
                    return EqualityFormulaSchema(a_term, b_term)

                assert isinstance(a_term, Term)
                assert isinstance(b_term, Term)
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

            b_form = self.parse_formula(parse_schema=parse_schema)
            self.index - 1

            if not self.is_at_end() and self.peek() == MiscToken.right_parenthesis:
                self.advance()

                if parse_schema:
                    assert isinstance(a_form, FormulaSchema)
                    assert isinstance(b_form, FormulaSchema)
                    return ConnectiveFormulaSchema(connective, a_form, b_form)

                assert isinstance(a_form, Formula)
                assert isinstance(b_form, Formula)
                return ConnectiveFormula(connective, a_form, b_form)

            raise self.error('Unclosed parentheses for binary formula', i_first_token=i_start, i_last_token=self.index - 1)

        raise self.error('Unexpected token')

    @overload
    def parse_negation_formula(self, *, parse_schema: Literal[False]) -> NegationFormula: ...
    @overload
    def parse_negation_formula(self, *, parse_schema: Literal[True]) -> NegationFormulaSchema: ...
    @overload
    def parse_negation_formula(self, *, parse_schema: bool) -> NegationFormula | NegationFormulaSchema: ...
    def parse_negation_formula(self, *, parse_schema: bool) -> NegationFormula | NegationFormulaSchema:
        assert self.peek() == UnaryConnective.negation
        self.advance()

        if parse_schema:
            return NegationFormulaSchema(self.parse_formula(parse_schema=True))

        return NegationFormula(self.parse_formula(parse_schema=False))

    @overload
    def parse_quantifier_formula(self, *, parse_schema: Literal[False]) -> QuantifierFormula: ...
    @overload
    def parse_quantifier_formula(self, *, parse_schema: Literal[True]) -> QuantifierFormulaSchema: ...
    @overload
    def parse_quantifier_formula(self, *, parse_schema: bool) -> QuantifierFormula | QuantifierFormulaSchema: ...
    def parse_quantifier_formula(self, *, parse_schema: bool) -> QuantifierFormula | QuantifierFormulaSchema:
        q = self.peek()
        assert isinstance(q, Quantifier)

        i_start = self.index
        self.advance()

        if self.is_at_end() or not isinstance(self.peek(), LatinIdentifier):
            raise self.error('Expected a variable after the quantifier', i_first_token=i_start)

        var = self.parse_variable(parse_schema=parse_schema)

        if not self.is_at_end() and self.peek() == MiscToken.dot:
            self.advance()
        else:
            raise self.error('Expected dot after variable', i_first_token=i_start)

        if parse_schema:
            assert isinstance(var, VariablePlaceholder)
            return QuantifierFormulaSchema(q, var, self.parse_formula(parse_schema=True))

        assert isinstance(var, Variable)
        return QuantifierFormula(q, var, self.parse_formula(parse_schema=False))

    @overload
    def parse_formula(self, *, parse_schema: Literal[False]) -> Formula: ...
    @overload
    def parse_formula(self, *, parse_schema: Literal[True]) -> FormulaSchema: ...
    @overload
    def parse_formula(self, *, parse_schema: bool) -> Formula | FormulaSchema: ...
    def parse_formula(self, *, parse_schema: bool) -> Formula | FormulaSchema:
        match self.peek():
            case PropConstant():
                return self.parse_constant_formula()

            case Quantifier():
                return self.parse_quantifier_formula(parse_schema=parse_schema)

            case MiscToken.left_parenthesis:
                return self.parse_binary_formula(parse_schema=parse_schema)

            case UnaryConnective.negation:
                return self.parse_negation_formula(parse_schema=parse_schema)

            case PredicateSymbolToken():
                if parse_schema:
                    self.error('No predicate formulas allowed in schemas')

                arity = self.signature.get_predicate_arity(str(self.peek()))
                return PredicateFormula(*self._parse_function_like(arity, parse_schema=parse_schema))

            case GreekIdentifier():
                if parse_schema:
                    return self.parse_formula_placeholder()

                raise self.error('Formula placeholders are only allowed in schemas')

            case _:
                raise self.error('Unexpected token')

    def parse_premise(self) -> NaturalDeductionPremise:
        discharge: FormulaSchema | None = None
        start = self.index

        if self.peek() == MiscToken.left_bracket:
            self.advance()
            discharge = self.parse_formula(parse_schema=True)

            if self.peek() == MiscToken.right_bracket:
                self.advance_and_skip_spaces()
            else:
                raise self.error('Unclosed brackets for discharge schemas', i_first_token=start)

        main = self.parse_formula(parse_schema=True)
        self.skip_spaces()
        return NaturalDeductionPremise(main, discharge)

    def iter_premises(self) -> Iterable[NaturalDeductionPremise]:
        for _ in self.iter_parse_premise_positions(RuleConnective.sequent, MiscToken.comma):
            self.skip_spaces()
            yield self.parse_premise()
            self.skip_spaces()

    def parse_rule(self) -> NaturalDeductionRule:
        name = self.parse_rule_name(MiscToken.left_parenthesis, MiscToken.right_parenthesis)
        self.advance_and_skip_spaces()
        premises = list(self.iter_premises())
        self.advance_and_skip_spaces()
        return NaturalDeductionRule(name, premises, self.parse_formula(parse_schema=True))


def parse_variable(string: str) -> Variable:
    tokens = tokenize_fol_string(EMPTY_SIGNATURE, string)

    with FOLParser(tokens, EMPTY_SIGNATURE) as parser:
        return parser.parse_variable(parse_schema=False)


def parse_term(signature: FOLSignature, string: str) -> Term:
    tokens = tokenize_fol_string(signature, string)

    with FOLParser(tokens, signature) as parser:
        return parser.parse_term(parse_schema=False)


def parse_formula(signature: FOLSignature, string: str) -> Formula:
    tokens = tokenize_fol_string(signature, string)

    with FOLParser(tokens, signature) as parser:
        return parser.parse_formula(parse_schema=False)


def parse_formula_schema(string: str) -> FormulaSchema:
    tokens = tokenize_fol_string(EMPTY_SIGNATURE, string)

    with FOLParser(tokens, EMPTY_SIGNATURE) as parser:
        return parser.parse_formula(parse_schema=True)


def parse_propositional_formula(string: str) -> Formula:
    return parse_formula(propositional_signature, string)


def parse_formula_placeholder(string: str) -> FormulaPlaceholder:
    tokens = tokenize_fol_string(EMPTY_SIGNATURE, string)

    with FOLParser(tokens, EMPTY_SIGNATURE) as parser:
        return parser.parse_formula_placeholder()


def parse_marker(string: str) -> Marker:
    tokens = tokenize_fol_string(EMPTY_SIGNATURE, string)

    with FOLParser(tokens, EMPTY_SIGNATURE) as parser:
        return parser.parse_marker()


def parse_natural_deduction_rule(string: str) -> NaturalDeductionRule:
    tokens = tokenize_fol_string(EMPTY_SIGNATURE, string)

    with FOLParser(tokens, EMPTY_SIGNATURE) as parser:
        return parser.parse_rule()
